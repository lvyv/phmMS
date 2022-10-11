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
from random import random

from fastapi import APIRouter
from typing import Optional

from phmconfig import constants
from phmconfig.timeUtils import TimeUtils
from physics.test import utils

router = APIRouter(
    prefix="/api/v1/mock",
    tags=["数据资源模拟数据"],
    responses={404: {"description": "Not found"}},
)


# 数据模拟类
@router.post("/zbMetric")
async def getZbMetric(equipTypeCode: Optional[str] = None, equipCode: Optional[str] = None,
                      equipName: Optional[str] = None):
    ret = {
        "result": [{
            "equipCode": "B001", "equipName": "电池1", "equipTypeCode": "N0001",
            "measurePoints": [{"pointCode": "M0001", "pointName": "容量", "pointUnit": "%"}]
        },
            {
                "equipCode": "B002", "equipName": "电池2", "equipTypeCode": "N0001",
                "measurePoints": [{"pointCode": "M0015", "pointName": "容量", "pointUnit": "%"}]
            }
        ]
    }
    return ret


@router.post("/zbData")
async def getZbData(equipCode, metricName, startTime, endTime, interval: Optional[str] = None):
    """
    模拟装备数据
    :param equipCode:
    :param metricName:
    :param startTime:
    :param endTime:
    :param interval:
    :return:
    """
    if True:
        return utils.convert(equipCode, metricName, startTime, endTime, constants.EQUIP_DATA_MAX_POINT)

    # 根据开始数据 与 结束时间生成 时间序列
    skipK = 1
    maxPoints = int(constants.EQUIP_DATA_MAX_POINT / skipK)
    if interval.endswith("M"):
        if interval.find(".") > 0:
            # 秒
            step = float(interval.replace("M", ""))
            interval = int(step * 60) * skipK
            pass
        else:
            # 分
            step = int(interval.replace("M", ""))
            interval = step * 60 * skipK
            pass
    elif interval.endswith("H"):
        step = int(interval.replace("H", ""))
        interval = step * 3600 * skipK
        pass
    elif interval.endswith("D"):
        step = int(interval.replace("D", ""))
        interval = step * 24 * 3600 * skipK
        pass

    genTime = []
    start = TimeUtils.convert_time_stamp(startTime)
    end = TimeUtils.convert_time_stamp(endTime)

    for inc in range(maxPoints):
        genTime.append(TimeUtils.convert_time_str(start + inc * interval * 1000))

    # 生成模拟数据
    ret = {
        "code": "success",
        "result": []
    }
    # 通过传入的设备编码
    devs = equipCode.split(",")
    tags = metricName.split(",")
    tagNumber = 1
    for dev in devs:
        genDev = {
            "equipCode": dev,
            "equipName": "电池" + dev,
            "equipData": []
        }
        for tag in tags:
            genTag = {
                "metricName": tag,
                "metricCode": "M00" + str(tagNumber),
                "metricData": []
            }

            for inx in range(maxPoints):
                genTag["metricData"].append({
                    "timestamp": genTime[inx],
                    "metricValue": int(random() * 100) if constants.MOCK_ZB_DATA_ALL_ZERO is False else 0
                })

            genDev["equipData"].append(genTag)

            tagNumber = tagNumber + 1
        ret["result"].append(genDev)

    return ret


@router.get("/zbMetricByTypeCode")
async def getZbMetricByTypeCode(equipTypeCode: Optional[str] = None):
    """
    模拟测点数据
    :param equipTypeCode:
    :return:
    """
    ret = {"result": {"data": []}}
    mockPointsName = ["容量", "健康指标", "最大温度", "最小温度", "电压不平衡度", "剩余寿命", "开路电压", "端电压",
                      "内阻不平衡度", "电池单元的最大开路电压", "电池单元的最小开路电压", "电池单元的最大端电压", "内阻",
                      "电池单元的最小端电压", "电池单元的均值端电压", "电池组的环境温度（存在多个测点）", "电池单元端电压集合",
                      "电池单元容量集合", "健康状态", "冲放电电流",
                      "环境温度", "充电次数", "工作温度", "测量的电流", "测量的电压","充电电流","充电电压"]
    for item in mockPointsName:
        ret["result"]["data"].append({"unit": "", "pointName": item})
    return ret
