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
controller layer
=========================

controller层，负责电池模型调用路由分发.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from fastapi import APIRouter, Depends
from services.vrlaBatteryService import VRLABatteryService
from utils.service_result import handle_result, ServiceResult
from utils.app_exceptions import AppException
from phmconfig.database import get_db
from pydantic import BaseModel

import json
import logging

router = APIRouter(
    prefix="/api/v1/phm/vrla",
    tags=["阀控铅酸蓄电池模型"],
    responses={404: {"description": "Not found"}},
)


# 电池健康模型的前端接口，该层接口可以实现模型与调用方解耦，并添加负载均衡等扩展功能。

# 1.健康评估模型，即根据输入设备的MVs，定义和解算SOH。
class SohInputParams(BaseModel):
    devices: str = '["d1", "d2"]'  # json string
    tags: str = '["t1", "t2"]'  # json string
    startts: int  # timestamp ms
    endts: int  # timestamp ms


@router.post("/soh")
async def call_soh(sohin: SohInputParams, db: get_db = Depends()):
    """
    健康评估模型

    :param sohin: 计算设备的soh需要的参数。
    :type: SohInputParams。
    :param db: 数据库连接。
    :type: sqlalchemy.orm.sessionmaker。
    :return:
    :rtype:
    """
    try:
        bs = VRLABatteryService(db)
        res = await bs.soh(json.loads(sohin.devices), json.loads(sohin.tags), sohin.startts, sohin.endts)
    except json.decoder.JSONDecodeError:
        res = ServiceResult(AppException.HttpRequestParamsIllegal())
    return handle_result(res)


# 2.工况判别模型，即主要利用聚类方法实现MVs的聚类分析。
@router.post("/cluster")
async def cluster(sohin: SohInputParams, displayType: str, db: get_db = Depends()):
    try:
        bs = VRLABatteryService(db)
        res = await bs.cluster(json.loads(sohin.devices), json.loads(sohin.tags), sohin.startts,
                               sohin.endts, displayType)
    except json.decoder.JSONDecodeError:
        res = ServiceResult(AppException.HttpRequestParamsIllegal)
    return handle_result(res)