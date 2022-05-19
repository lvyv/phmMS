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
    try:
        MqttClient().start()
    except Exception as e:
        print(e)
    finally:
        pass


threading.Thread(target=startMqtt()).start()


def write_back_history_result(client, reqid):
    # 回写历史状态
    params = {'reqid': reqid, 'res': "settled"}
    client.put(f'{bcf.URL_MD_WRITE_REQ_HISTORY}', params=params)


def publish_data_to_iot(reqid, data):
    # 发布遥测数据到IOT
    try:
        MqttClient().publish(json.dumps({"reqid": reqid, "sohres": data}))
    except Exception as e:
        print(e)
    finally:
        pass


def post_process_vrla_soh(reqid, items):
    with httpx.Client(timeout=None, verify=False) as client:
        write_back_history_result(client, reqid)
        # 写回指标统计数据库表
        for item in items:
            keys = item.keys()
            eqi = {
                "did": item['did'] if 'did' in keys else "unknown",
                "dclz": "BATTERY",
                "remainLife": item['remainLife'] if "remainLife" in keys else 0,
                "voc": item['voc'] if "voc" in keys else 0,
                "workVoc": item['workVoc'] if "workVoc" in keys else 0,
                "current": item['current'] if "current" in keys else 0,
                "minTemp": item['minTemp'] if "minTemp" in keys else 0,
                "maxTemp": item['maxTemp'] if "maxTemp" in keys else 0,
                "cellMaxVoc": item['cellMaxVoc'] if "cellMaxVoc" in keys else 0,
                "cellMinVoc": item['cellMinVoc'] if "cellMinVoc" in keys else 0,
                "cellMaxVol": item['cellMaxVol'] if "cellMaxVol" in keys else 0,
                "cellMinVol": item['cellMinVol'] if "cellMinVol" in keys else 0,
                "cellAvgVol": item['cellAvgVol'] if "cellAvgVol" in keys else 0,
                "envTemp": item['envTemp'] if "envTemp" in keys else "[0, 0]",
                "cellVol": item['cellVol'] if "cellVol" in keys else "[0, 0, 0, 0, 0, 0]",
                "cellSoc": item['cellSoc'] if "cellSoc" in keys else "[0, 0, 0, 0, 0, 0]",
                "soh": item['soh'] if "soh" in keys else 0,
                "soc": item['soc'] if 'soc' in keys else 0,
                "imbalance": item['imbalance'] if 'imbalance' in keys else 0,
                "ts": item['ts'] if 'ts' in keys else 0,
                "state": item['state'] if 'state' in keys else 0
            }
            client.post(f'{bcf.URL_MD_WRITE_EVAL}', json=eqi)

        publish_data_to_iot(reqid, items)


def post_process_vrla_cluster(reqid, sohres, displayType):
    with httpx.Client(timeout=None, verify=False) as client:

        write_back_history_result(client, reqid)

        # 聚类模型需要数据转换
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


def post_process_vrla_relation(reqid, items):
    with httpx.Client(timeout=None, verify=False) as client:

        write_back_history_result(client, reqid)

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

        publish_data_to_iot(reqid, items)


# time intensive tasks
def soh_task(sohin, reqid):
    # 下载装备数据
    dataS = dataCenter.download_zb_data(sohin.devices, sohin.tags, sohin.startts, sohin.endts)
    # 获取测点映射
    devices = json.loads(sohin.devices)
    if len(devices) > 0:
        mappingS = dataCenter.query_metric_mapping(devices[0])
    else:
        mappingS = dataCenter.query_metric_mapping()
    # 测点反转
    convertMapping = {}
    if mappingS is not None:
        for k, v in mappingS.items():
            convertMapping[v] = k

    # 计算SOH
    res = phm.calculate_soh(dataS, convertMapping)

    # 处理结果
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
    devices: str = '[\"B001\", \"B002\"]'  # json string
    tags: str = '[\"soc\",\"soh\"]'  # json string
    startts: int = 1652170492000  # timestamp ms
    endts: int = 1652256892000  # timestamp ms


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
