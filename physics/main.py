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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from physics.vrla.soh import evaluate_soh as vrla_soh
from phmconfig import basiccfg as bcf
import concurrent.futures
import httpx
import json
import logging
import paho.mqtt.client as mqtt_client


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

# 线程池初始化
executor_ = concurrent.futures.ThreadPoolExecutor(max_workers=5)


def post_process_vrla_soh(reqid, sohres):
    with httpx.Client(timeout=None, verify=False) as client:
        params = {'reqid': reqid, 'res': json.dumps(sohres)}
        # 1.写回请求响应数据库表
        r = client.put(f'{bcf.URL_RESULT_WRITEBACK}', params=params)

        # 2.写回指标统计数据库表
        items = json.loads(params['res'])
        for did in items.keys():
            eqitem = items[did]
            eqi = {
                "did": did,
                "devclass": "BATTERY",  # FIXME
                "dis_voltage": 0,
                "dis_current": 0,
                "dis_resistance": 0,
                "dis_temperature": 0,
                "dis_dischargecycles": 0,
                "chg_voltage": 0,
                "chg_current": 0,
                "chg_resistance": 0,
                "chg_temperature": 0,
                "chg_dischargecycles": 0,
                "soh": eqitem['soh'],
                "soc": eqitem['extend']['soc'],
                "Rimbalance": eqitem['extend']['Rimbalance'],
                "ts": eqitem['ts']
            }
            r = client.post(f'{bcf.URL_POST_EQUIPMENT}', json=eqi)

        # 3.推送MQTT
        mqttclient = mqtt_client.Client('mqttcid')
        mqttclient.username_pw_set('tstusr12', 'pwdtst')
        mqttclient.connect('test.mosquitto.org', 1883)
        mqttclient.publish('phm/vlra_7891/soh', {"reqid": reqid, "sohres": sohres})

        logging.info(r)


# time intensive tasks
def soh_task(sohin, reqid):
    # 查询传入的设备号是什么样的设备类型（要求传入的设备号都是同样的设备类型）
    devids = json.loads(sohin.devices)
    devtype = bcf.DT_VRLA
    res = None
    if devtype == bcf.DT_VRLA:          # 阀控铅酸电池
        res = vrla_soh(devids)
        post_process_vrla_soh(reqid, res)               # 写两个库表（req_history, public.xc_equipment），发mqtt
    elif devtype == bcf.DT_CELLPACK:    # UPS电池组
        pass
    else:
        pass
    return res


# IF11:REST MODEL 外部接口-phmMD与phmMS之间接口
class SohInputParams(BaseModel):
    devices: str = '[]'     # json string
    tags: str = '[]'        # json string
    startts: int            # timestamp ms
    endts: int              # timestamp ms


@app.post("/api/v1/soh")
async def calculate_soh(sohin: SohInputParams, reqid: int):
    """模拟耗时的机器学习任务"""
    executor_.submit(soh_task, sohin, reqid)
    return {'task': reqid, 'status': 'submitted to work thread.'}
