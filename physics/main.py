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


# time intensive tasks
def soh_task(sohin, reqid):
    with httpx.Client(timeout=None, verify=False) as client:
        # 查询传入的设备号是什么样的设备类型（要求传入的设备号都是同样的设备类型）
        devids = json.loads(sohin.devices)
        devid = devids[0]
        params = {'deviceid': devid}
        # r = client.get(f'{bcf.URL_DEVICETYPE}', params=params)
        # jso = json.loads(str(r.content, 'utf-8'))
        # devtype = jso['type']
        # logging.info(jso)
        # 根据查询到的设备类型调用相应的模型计算soh值

        devtype = bcf.DT_VRLA
        res = 'threading end result.'
        if devtype == bcf.DT_VRLA:          # 阀控铅酸电池
            res = vrla_soh(devids)
        elif devtype == bcf.DT_CELLPACK:    # UPS电池组
            res = bcf.DT_CELLPACK
        params = {'reqid': reqid, 'res':  json.dumps(res)}
        r = client.put(f'{bcf.URL_RESULT_WRITEBACK}', params=params)
        logging.info(r)
        return 0


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
