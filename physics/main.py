#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 The CASICloud Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

"""
=========================
entrypoint of the app
=========================

模型微服务入口.
"""
import threading
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from phmconfig import constants as bcf
import concurrent.futures
import httpx
import json
import logging
from physics.transport.mqttclient import MqttClient
from fastapi.staticfiles import StaticFiles
from physics.test import mock_zb_router
from physics.vrla import phm
from physics.transport import dataCenter
from services.convert.cluster_display_util import ClusterDisplayUtil
from phmconfig.timeUtils import TimeUtils

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
app = FastAPI()

# 支持跨域
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory='../swagger_ui_dep/static'), name='static')

# 线程池初始化
executor_ = concurrent.futures.ThreadPoolExecutor(max_workers=5)


def startMqtt():
    MqttClient().start()


threading.Thread(target=startMqtt()).start()


def write_back_history_result(client, reqid):
    # 回写历史状态
    params = {'reqid': reqid, 'res': "settled"}
    client.put(f'{bcf.URL_MD_WRITE_REQ_HISTORY}', params=params)


def publish_data_to_iot(reqid, data):
    # 发布遥测数据到IOT
    MqttClient().publish(json.dumps({"reqid": reqid, "sohres": data}))


def post_process_vrla_soh(reqid, sohres):
    with httpx.Client(timeout=None, verify=False) as client:
        write_back_history_result(client, reqid)

        # 数据转换
        items = phm.soh_convert(sohres)

        # 写回指标统计数据库表
        for did in items.keys():
            eqitem = items[did]
            eqi = {
                "did": did,
                "dclz": "BATTERY",
                "remainLife": 0,
                "voc": 0,
                "workVoc": 0,
                "current": 0,
                "minTemp": 0,
                "maxTemp": 0,
                "cellMaxVoc": 0,
                "cellMinVoc": 0,
                "cellMaxVol": 0,
                "cellMinVol": 0,
                "cellAvgVol": 0,
                "envTemp": "[19, 20]",
                "cellVol": "[20, 21, 22, 20, 21, 22]",
                "cellSoc": "[20, 22, 22, 22, 22, 23]",
                "soh": eqitem['soh'],
                "soc": eqitem['extend']['soc'],
                "imbalance": eqitem['extend']['Rimbalance'],
                "ts": eqitem['ts'],
                "state": 1
            }
            client.post(f'{bcf.URL_MD_WRITE_EVAL}', json=eqi)

        publish_data_to_iot(reqid, sohres)


def post_process_vrla_cluster(reqid, sohres, displayType):
    with httpx.Client(timeout=None, verify=False) as client:

        write_back_history_result(client, reqid)

        # 数据转换
        items = phm.cluster_convert(sohres)

        # 将数据写入数据库
        for did in items.keys():
            eqi = {
                "reqId": reqid,
                "ts": int(time.time() * 1000),
                "name": items[did][0],
                "size": 0,  # items[did][1],
                "color": items[did][2],
                "shape": 0,  # items[did][3],
                "x": items[did][4],
                "y": items[did][5],
                "z": 0  # items[did][6]
            }

            if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D]:
                eqi["size"] = items[did][1]

            if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                               ClusterDisplayUtil.DISPLAY_AGG2D]:
                eqi["shape"] = items[did][3]

            if displayType in [ClusterDisplayUtil.DISPLAY_3D, ClusterDisplayUtil.DISPLAY_AGG3D]:
                eqi["z"] = items[did][6]

            client.post(bcf.URL_MD_WRITE_CLUSTER, json=eqi)
            time.sleep(0.1)

        publish_data_to_iot(reqid, sohres)


def post_process_vrla_relation(reqid, sohres):
    with httpx.Client(timeout=None, verify=False) as client:

        write_back_history_result(client, reqid)

        # 数据转换
        items = phm.relate_convert(sohres)

        # 写回指标统计数据库表
        for did in items.keys():
            eqitem = items[did]
            for index, item in enumerate(eqitem["lag"]):
                eqi = {
                    "reqId": reqid,
                    "lag": item,
                    "value": eqitem["value"][index],
                    "ts": int(time.time() * 1000),
                }
                client.post(f'{bcf.URL_MD_WRITE_SELF_RELATION}', json=eqi)

        publish_data_to_iot(reqid, sohres)


# time intensive tasks
def soh_task(sohin, reqid):
    dataS = dataCenter.download_zb_data(sohin.devices, sohin.tags, sohin.startts, sohin.endts)
    res = phm.calculate_soh(dataS, json.loads(sohin.devices))
    post_process_vrla_soh(reqid, res)


def cluster_task(clusterin, reqid, displayType):
    dataS = dataCenter.download_zb_data(clusterin.devices, clusterin.tags, clusterin.startts, clusterin.endts)
    res = phm.calculate_cluster(dataS, displayType)
    post_process_vrla_cluster(reqid, res, displayType)


def relation_task(relationin, reqid, leftTag, rightTag, step, unit):
    dataS = dataCenter.download_zb_data(relationin.devices, relationin.tags, relationin.startts, relationin.endts)
    res = phm.calculate_relate(dataS, leftTag, rightTag, step, unit)
    post_process_vrla_relation(reqid, res)


# IF11:REST MODEL 外部接口-phmMD与phmMS之间接口
class SohInputParams(BaseModel):
    devices: str = '[]'  # json string
    tags: str = '[]'  # json string
    startts: int  # timestamp ms
    endts: int  # timestamp ms


@app.post("/api/v1/soh")
async def calculate_soh(sohin: SohInputParams, reqid: int):
    """模拟耗时的机器学习任务"""
    executor_.submit(soh_task, sohin, reqid)
    return {'task': reqid, 'status': 'submitted to work thread.'}


@app.post("/api/v1/cluster")
async def calculate_cluster(sohin: SohInputParams, reqid: int, displayType: str):
    """模拟耗时的机器学习任务"""
    executor_.submit(cluster_task, sohin, reqid, displayType)
    return {'task': reqid, 'status': 'submitted to work thread.'}


@app.post("/api/v1/relation")
async def calculate_relation(sohin: SohInputParams, reqid: int, leftTag: int, rightTag: int, step: int, unit: int):
    executor_.submit(relation_task, sohin, reqid, leftTag, rightTag, step, unit)
    return {'task': reqid, 'status': 'submitted to work thread.'}


def get_metric_task(equipCode):
    datas = dataCenter.download_zb_metric_from(equipCode)
    dataCenter.process_zb_metric_from(datas)
    return datas


@app.post("/api/v1/get_metric")
async def mock_metrics(equipCode):
    executor_.submit(get_metric_task, equipCode)
    return {"status": "submitted to work thread."}


def get_metric_data_task(metricCode, startTime, endTime):
    start = TimeUtils.convert_time_str(int(startTime))
    end = TimeUtils.convert_time_str(int(endTime))
    interval = TimeUtils.get_time_interval(int(startTime), int(endTime))
    datas = dataCenter.download_zb_history_data_from(metricCode, start, end, interval)
    dataCenter.process_zb_history_data_from(datas)
    return datas


@app.post("/api/v1/get_data")
async def mock_metric_data(metricCode, startTime, endTime):
    executor_.submit(get_metric_data_task, metricCode, startTime, endTime)
    return {"status": "submitted to work thread."}


app.include_router(mock_zb_router.router)
