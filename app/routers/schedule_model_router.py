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
    tags=["模型调度"],
    responses={404: {"description": "Not found"}},
)


# 电池健康模型的前端接口，该层接口可以实现模型与调用方解耦，并添加负载均衡等扩展功能。

# 1.健康评估模型，即根据输入设备的MVs，定义和解算SOH。
class SohInputParams(BaseModel):
    devices: str = '["d1", "d2"]'  # json string
    tags: str = '["t1", "t2"]'  # json string
    startts: int  # timestamp ms
    endts: int  # timestamp ms
    equipTypeCode: str = ''


@router.post("/soh")
async def call_soh(sohin: SohInputParams, displayType: str, db: get_db = Depends()):
    """
    健康评估模型调度

    :param displayType: 模型计算类型
    :param sohin: 计算设备的soh需要的参数。
    :type: SohInputParams。
    :param db: 数据库连接。
    :type: sqlalchemy.orm.sessionmaker。
    :return:
    :rtype:
    """
    try:
        bs = VRLABatteryService(db)
        res = await bs.soh(sohin.equipTypeCode, json.loads(sohin.devices), json.loads(sohin.tags), sohin.startts, sohin.endts, displayType)
    except json.decoder.JSONDecodeError:
        res = ServiceResult(AppException.HttpRequestParamsIllegal())
    return handle_result(res)


# 2.工况判别模型，即主要利用聚类方法实现MVs的聚类分析。
@router.post("/cluster")
async def cluster(sohin: SohInputParams, displayType: str, db: get_db = Depends()):
    """
    聚类模型调度
    :param sohin: 参与聚类模型参数
    :param displayType: 聚类模型类型
    :param db: 数据库连接
    :return:
    """
    try:
        bs = VRLABatteryService(db)
        res = await bs.cluster(sohin.equipTypeCode, json.loads(sohin.devices), json.loads(sohin.tags), sohin.startts,
                               sohin.endts, displayType)
    except json.decoder.JSONDecodeError:
        res = ServiceResult(AppException.HttpRequestParamsIllegal)
    return handle_result(res)


@router.post("/relation")
async def relation(sohin: SohInputParams, subFrom: int, subTo: int, db: get_db = Depends()):
    """
    自相关模型调度
    :param sohin:  参与自相关模型计算参数
    :param subFrom:  计算时间窗开始时间
    :param subTo:    计算时间窗结束时间
    :param db:    数据库连接
    :return:
    """
    try:
        bs = VRLABatteryService(db)
        res = await bs.relation(sohin.equipTypeCode, json.loads(sohin.devices), json.loads(sohin.tags), sohin.startts,
                                sohin.endts, subFrom, subTo)
    except json.decoder.JSONDecodeError:
        res = ServiceResult(AppException.HttpRequestParamsIllegal)
    return handle_result(res)
