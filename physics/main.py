#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from phmconfig import constants as bcf
import concurrent.futures
import httpx
import json
import logging
# from physics.transport.mqttclient import MqttClient
from fastapi.staticfiles import StaticFiles
from physics.test import mock_zb_router
from physics.vrla import phm
from physics.transport import dataCenter
from physics.router import public_router
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


# def startMqtt():
#     try:
#         MqttClient().start()
#     except Exception as e:
#         print(e)
#     finally:
#         pass


# threading.Thread(target=startMqtt()).start()


def write_back_history_result(reqid):
    with httpx.Client(timeout=None, verify=False) as client:
        # 回写历史状态
        params = {'reqid': reqid, 'res': "settled"}
        client.put(f'{bcf.URL_MD_WRITE_REQ_HISTORY}', params=params)


# def publish_data_to_iot(reqid, data):
#     # 发布遥测数据到IOT
#     try:
#         MqttClient().publish(json.dumps({"reqid": reqid, "sohres": data}))
#     except Exception as e:
#         print(e)
#     finally:
#         pass


def post_process_vrla_soh(reqid, items):

    write_back_history_result(reqid)

    with httpx.Client(timeout=None, verify=False) as client:
        client.post(f'{bcf.URL_MD_WRITE_EVAL_BATCH}', params={"reqid": reqid},  json={"items": json.dumps(items)})

    # publish_data_to_iot(reqid, items)


def post_process_vrla_cluster(reqid, sohres, displayType):

    write_back_history_result(reqid)

    with httpx.Client(timeout=None, verify=False) as client:
        # 聚类模型需要数据转换
        items = phm.cluster_convert(sohres)
        client.post(bcf.URL_MD_WRITE_CLUSTER_BATCH,
                    params={"reqid": reqid, "displayType": displayType},
                    json={"items": json.dumps(items)})

    # publish_data_to_iot(reqid, sohres)


def post_process_vrla_relation(reqid, items):

    write_back_history_result(reqid)

    with httpx.Client(timeout=None, verify=False) as client:
        client.post(f'{bcf.URL_MD_WRITE_SELF_RELATION_BATCH}',
                    params={"reqid": reqid},
                    json={"items": json.dumps(items)})

    # publish_data_to_iot(reqid, items)


# time intensive tasks
def soh_task(sohin, reqid):
    # 下载装备数据
    dataS = dataCenter.download_zb_data(sohin.devices, sohin.tags, sohin.startts, sohin.endts)
    try:
        mappingS = dataCenter.query_metric_mapping(sohin.equipTypeCode)
        convertMapping = {}
        if mappingS is not None:
            for k, v in mappingS.items():
                convertMapping[v] = k
        logging.info("测点映射:" + json.dumps(convertMapping, ensure_ascii=False))

        dev_type = dataCenter.query_equip_type_by_equip_type_code(sohin.equipTypeCode)
        # 计算SOH
        res = phm.calculate_soh(dataS, convertMapping, dev_type)
        # 处理结果
        post_process_vrla_soh(reqid, res)
    except Exception as e:
        logging.error(e)
    logging.info("计算SOH完成")


def cluster_task(clusterin, reqid, displayType):
    dataS = dataCenter.download_zb_data(clusterin.devices, clusterin.tags, clusterin.startts, clusterin.endts)
    try:
        res = phm.calculate_cluster(dataS, displayType)
        post_process_vrla_cluster(reqid, res, displayType)
    except Exception as e:
        logging.error(e)
    logging.info("聚类计算完成: " + displayType)


def relation_task(relationin, reqid, subFrom, subTo):
    if subFrom == -1 and subTo == -1:
        logging.info("relation param, startTime: " + TimeUtils.convert_time_str(relationin.startts) +
                     " endTime: " + TimeUtils.convert_time_str(relationin.endts) +
                     " subFrom: " + str(subFrom) +
                     " subTo: " + str(subTo))
    else:
        logging.info("relation param, startTime: " + TimeUtils.convert_time_str(relationin.startts) +
                     " endTime: " + TimeUtils.convert_time_str(relationin.endts) +
                     " subFrom: " + TimeUtils.convert_time_str(subFrom) +
                     " subTo: " + TimeUtils.convert_time_str(subTo))
    dataS = dataCenter.download_zb_data(relationin.devices, relationin.tags, relationin.startts, relationin.endts)
    try:
        res = phm.calculate_relate(dataS, subFrom, subTo)
        post_process_vrla_relation(reqid, res)
    except Exception as e:
        logging.error(e)
    logging.info("自相关计算完成")


# IF11:REST MODEL 外部接口-phmMD与phmMS之间接口
class SohInputParams(BaseModel):
    devices: str = '[\"B001\", \"B002\"]'  # json string
    tags: str = '[\"soc\",\"soh\"]'  # json string
    startts: int = 1652170492000  # timestamp ms
    endts: int = 1652256892000  # timestamp ms
    equipTypeCode: str = ''


@app.post("/api/v1/soh")
async def calculate_soh(sohin: SohInputParams, reqid: int):
    """提交soh任务"""
    executor_.submit(soh_task, sohin, reqid)
    return {'task': reqid, 'status': 'submitted to work thread.'}


@app.post("/api/v1/cluster")
async def calculate_cluster(sohin: SohInputParams, reqid: int, displayType: str):
    """提交聚类任务"""
    executor_.submit(cluster_task, sohin, reqid, displayType)
    return {'task': reqid, 'status': 'submitted to work thread.'}


@app.post("/api/v1/relation")
async def calculate_relation(sohin: SohInputParams, reqid: int, subFrom: int, subTo: int):
    """提交自相关任务"""
    executor_.submit(relation_task, sohin, reqid, subFrom, subTo)
    return {'task': reqid, 'status': 'submitted to work thread.'}


app.include_router(mock_zb_router.router)
app.include_router(public_router.router)
