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
from services.convert.health_eval_util import HealthEvalUtil
from services.convert.self_relation_util import SelfRelationUtil
from services.equipTypeMappingService import EquipTypeMappingService
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.reqhistoryService import ReqHistoryService
from services.validate.publicModelValidate import PublicModelValidate
from utils.service_result import handle_result, ServiceResult

router = APIRouter(
    prefix="/api/v1/public/plugin",
    tags=["插件配置"],
    responses={404: {"description": "Not found"}},
)


# 获取装备类型
@router.get("/equipType")
async def getEquipTypeByPlugin(db: get_db = Depends()):
    """
        获取所有的装备类型
    """
    so = EquipTypeMappingService(db)
    result = ServiceResult(so.getAllEquipTypeMapping())
    return handle_result(result)


# 获取装备编码
@router.get("/equipCode")
async def getEquipCodeByPlugin(equipType, displayType, db: get_db = Depends()):
    """
    获取装备编码
    :param equipType:
            装备类型编码
    :param displayType:
            聚类类型
    :param db:
            数据库
    :return:
    """
    so = ReqHistoryService(db)
    result = so.get_equip_code(displayType)
    return handle_result(result)


# 获取装备编码
@router.get("/metric")
async def getMetricByPlugin(equipType, equipCode, displayType, db: get_db = Depends()):
    """
    获取装备测点
    :param equipType:
            装备编码类型
    :param equipCode:
            装备编码
    :param displayType:
            聚类类型
    :param db:
            数据库
    :return:
    """
    so = ReqHistoryService(db)
    result = so.get_equip_metric(equipCode, displayType)
    return handle_result(result)


# 获取时间段
@router.get("/timeSegment")
async def getTimeSegmentByPlugin(equipType, equipCode, metric, displayType, db: get_db = Depends()):
    """
      获取用于模型计算的时间段
    Parameters
    ----------
    equipType   装备类型编码
    equipCode   装备编码
    metric      测点名称
    displayType 模型类型
    db          db

    Returns
    -------

    """
    support, equipCode, metric = PublicModelValidate.support(equipCode, metric)
    if support is False:
        return "请输入不为空的设备编码或测点"

    so = ReqHistoryService(db)
    if displayType in [HealthEvalUtil.DISPLAY_HEALTH_EVAL]:
        # 评估界面获取所有测点的数据，用于评估计算 健康值，健康状态，电压不平衡度，内阻不平衡度
        result = MetricMappingService(db).get_all_mapping_by_equip_type_code(equipType)
        allMetrics = ",".join(metricName for metricName in result.values())
        result = so.get_time_segment(equipCode, allMetrics, displayType)
    else:
        result = so.get_time_segment(equipCode, metric, displayType)
    return handle_result(result)


# 删除时间段
@router.delete("/timeSegment")
async def deleteTimeSegmentByPlugin(equipType, equipCode, metric, displayType, timeSegment, db: get_db = Depends()):
    """
    删除历史计算时间记录
    :param equipType:
            装备类型编码
    :param equipCode:
            装备编码
    :param metric:
            测点名称
    :param displayType:
            模型类型
    :param timeSegment:
            参与历史计算时间段
    :param db:
            数据库
    :return:
    """
    support, equipCode, metric = PublicModelValidate.support(equipCode, metric)
    if support is False:
        return "请输入不为空的设备编码或测点"

    so = ReqHistoryService(db)
    if displayType in [HealthEvalUtil.DISPLAY_HEALTH_EVAL]:
        # 评估界面获取所有测点的数据，用于评估计算 健康值，健康状态，电压不平衡度，内阻不平衡度
        result = MetricMappingService(db).get_all_mapping_by_equip_type_code(equipType)
        allMetrics = ",".join(metricName for metricName in result.values())
        result = so.delete_time_segment(equipCode, allMetrics, timeSegment, displayType)
    else:
        result = so.delete_time_segment(equipCode, metric, timeSegment, displayType)
    return handle_result(result)


# 提供给 IOT-Json 插件测量标志
@router.get("/indicator")
async def getEquipTypeByPlugin():
    result = ServiceResult(["$equipType^$equipCode^$metrics^2D^$host", "$equipType^$equipCode^$metrics^3D^$host",
                            "$equipType^$equipCode^$metrics^AGG2D^$host", "$equipType^$equipCode^$metrics^AGG3D^$host",
                            "$equipType^$equipCode^$metrics^$timeSegment^SELF_RELATION^$host",
                            "$equipType^$equipCode^$metrics^SELF_POLYLINE^$host",
                            "$equipType^$equipCode^$metrics^SCATTER^$host",
                            "$equipType^$equipCode^$metrics^POLYLINE^$host",
                            "$equipType^$equipCode^SOH^EVAL^$host"])
    return handle_result(result)


@router.get("/timeSegment/params")
async def getParamsByPlugin(equipType, equipCode, metric, timeSegment, displayType, db: get_db = Depends()):
    """
        获取参与自相关模型计算的SUB时间段

    Parameters
    ----------
    equipType   装备类型编码
    equipCode   装备编码
    metric      测点名称
    timeSegment   参数模型计算的时间端
    displayType   模型类型
    db            db

    Returns
    -------

    """
    if displayType not in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
        return "不支持查询参数"
    support, equipCode, metric = PublicModelValidate.support(equipCode, metric)
    if support is False:
        return "请输入不为空的设备编码或测点"
    so = ReqHistoryService(db)
    result = so.get_params(equipCode, metric, timeSegment, displayType)
    return handle_result(result)


@router.get("/getReqHistory")
async def getReqHistoryByEquipType(equipType, db: get_db = Depends()):
    """
    获取历史记录
    :param equipType:
            装备类型编码
    :param db:
            数据库
    :return:
    """
    so = ReqHistoryService(db)
    result = so.get_all(equipType)
    return handle_result(result)


@router.delete("/delReqHistoryById")
async def delReqHistoryById(reqId: int, db: get_db = Depends()):
    """
    删除历史记录
    :param reqId:
            历史记录ID
    :param db:
            数据库
    :return:
    """
    so = ReqHistoryService(db)
    result = so.delete_by_id(reqId)
    return handle_result(result)
