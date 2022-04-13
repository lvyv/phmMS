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
from physics.vrla.soh import evaluate_soh as vrla_soh
from phmconfig import basiccfg as bcf
import concurrent.futures
import httpx
import json
import logging
from physics.mqttclient import MqttClient
from fastapi.staticfiles import StaticFiles
from physics.test import mock_zb_router
from physics.vibration import phm

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


def post_process_vrla_soh(reqid, sohres):
    with httpx.Client(timeout=None, verify=False) as client:
        params = {'reqid': reqid, 'res': "settled"}
        # 1.写回请求响应数据库表
        r = client.put(f'{bcf.URL_RESULT_WRITEBACK}', params=params)

        # 2.写回指标统计数据库表
        items = json.loads(json.dumps(sohres))
        for did in items.keys():
            eqitem = items[did]
            eqi = {
                "did": did,
                "dclz": "BATTERY",  # FIXME
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
            client.post(f'{bcf.URL_POST_EQUIPMENT}', json=eqi)
        MqttClient().publish(json.dumps({"reqid": reqid, "sohres": sohres}))
        logging.info(r)


def post_process_vrla_cluster(reqid, sohres, displayType):
    with httpx.Client(timeout=None, verify=False) as client:
        params = {'reqid': reqid, 'res': "settled"}
        r = client.put(f'{bcf.URL_RESULT_WRITEBACK}', params=params)
        logging.info(r)
        items = phm.model_convert(json.loads(sohres))

        for did in items.keys():
            eqi = {
                "reqId": reqid,
                "x": items[did][4],
                "y": items[did][5],
                "name": items[did][0],
                "size": items[did][1],
                "color": items[did][2],
                "shape": items[did][3],
                "ts": int(time.time() * 1000),
                "z": 0
            }
            if displayType in ["AGG3D", "3D"]:
                eqi["z"] = items[did][6]

            url = bcf.URL_POST_CLUSTER_PREFIX
            r = client.post(url, json=eqi)
            time.sleep(0.1)
            logging.info(r)
        MqttClient().publish(json.dumps({"reqid": reqid, "sohres": sohres}))


def post_process_vrla_relation(reqid, sohres):
    with httpx.Client(timeout=None, verify=False) as client:
        params = {'reqid': reqid, 'res': "settled"}
        # 1.写回请求响应数据库表
        r = client.put(f'{bcf.URL_RESULT_WRITEBACK}', params=params)

        # 2.写回指标统计数据库表
        items = json.loads(json.dumps(sohres))
        for did in items.keys():
            eqitem = items[did]
            eqi = {
                "reqId": reqid,
                "lag": (int(time.time() * 1000)) % 50,
                "value": 5,
                "ts": int(time.time() * 1000),
            }
            client.post(f'{bcf.URL_POST_SELF_RELATION}', json=eqi)
        MqttClient().publish(json.dumps({"reqid": reqid, "sohres": sohres}))
        logging.info(r)


# time intensive tasks
def soh_task(sohin, reqid):
    # 查询传入的设备号是什么样的设备类型（要求传入的设备号都是同样的设备类型）
    devids = json.loads(sohin.devices)
    devtype = bcf.DT_VRLA
    res = None
    if devtype == bcf.DT_VRLA:  # 阀控铅酸电池
        res = vrla_soh(devids)
        post_process_vrla_soh(reqid, res)
    elif devtype == bcf.DT_CELLPACK:  # UPS电池组
        pass
    else:
        pass
    return res


def cluster_task(clusterin, reqid, displayType):
    # TODO 聚类接口
    devids = json.loads(clusterin.devices)
    devtype = bcf.DT_VRLA
    res = None
    if devtype == bcf.DT_VRLA:  # 阀控铅酸电池
        dataS = phm.download_zb_data(clusterin.devices, clusterin.tags, clusterin.startts, clusterin.endts)
        if displayType in ["AGG3D", "3D"]:
            res = phm.model_invoke(dataS, 3)
        else:
            res = phm.model_invoke(dataS, 2)
        post_process_vrla_cluster(reqid, res, displayType)
    elif devtype == bcf.DT_CELLPACK:  # UPS电池组
        pass
    else:
        pass
    return res


def relation_task(relationin, reqid, leftTag, rightTag, step, unit):
    devids = json.loads(relationin.devices)
    devtype = bcf.DT_VRLA
    res = None
    if devtype == bcf.DT_VRLA:  # 阀控铅酸电池
        res = {"B001": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]},
               "B002": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]}}
        post_process_vrla_relation(reqid, res)
        pass
    elif devtype == bcf.DT_CELLPACK:  # UPS电池组
        pass
    else:
        pass
    return res


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


app.include_router(mock_zb_router.router)
