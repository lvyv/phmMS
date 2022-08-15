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
from typing import Optional

from services.configManagerService import ConfigManagerService
from services.dashboardManagerService import DashboardManagerService
from services.equipTypeMappingService import EquipTypeMappingService
from services.grafanaManagerService import GrafanaMangerService
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.reqhistoryService import ReqHistoryService
from utils.service_result import handle_result, ServiceResult

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getEquipType")
async def getEquipType(equipTypeCode: str, db: get_db = Depends()):
    """
    获取装备类型
    :param equipTypeCode:
            装备类型编码
    :param db:
            数据库
    :return:
    """
    so = EquipTypeMappingService(db)
    result = so.getEquipTypeMapping(equipTypeCode)
    return handle_result(ServiceResult(result))


# 根据装备类型获取mapping
@router.get("/getMapping")
async def getMapping(equipTypeCode: str, db: get_db = Depends()):
    """
    获取测点映射表
    :param equipTypeCode:
            装备类型编码
    :param db:
            数据库
    :return:
    """
    so = MetricMappingService(db)
    result = so.get_all_mapping_by_equip_type_code(equipTypeCode)
    return handle_result(ServiceResult(result))


@router.put("/updateHistoryRecord")
async def updateHistoryRecord(reqid: str, res: str, canDelete: Optional[bool] = False, db: get_db = Depends()):
    """
    更新历史记录
    :param canDelete:
            数据发送异常，删除请求历史
    :param reqid:
            历史记录ID
    :param res:
            结果状态
    :param db:
            数据库
    :return:
    """
    reqs = ReqHistoryService(db)
    if canDelete:
        result = reqs.delete_by_id(reqid)
    else:
        result = reqs.update_item(reqid, res)
    return handle_result(result)


# 获取装备健康大屏列表
@router.get("/dashboards")
async def get_trend_dashboard(query: Optional[str] = None, filter: Optional[str] = None):
    """
    获取装备健康大屏列表
    :param query:
            查询条件
    :param filter:
            过滤条件
    :return:
    """
    return DashboardManagerService.getDashboardList(query, filter)


# 修改装备大屏host地址
@router.get("/grafana/syncHost")
async def grafana_sync_host(host: Optional[str] = None,
                            timeSegmentLabel: Optional[str] = None,
                            username: Optional[str] = "admin", password: Optional[str] = "admin"):
    """
    修改ZBJK大屏Host地址
    :param host:
            MS 服务器地址 eg: https://ip:port
    :param timeSegmentLabel:
            大屏参与历史计算时间段标签名称
    :param username:
            grafana 用户名
    :param password:
            grafana 密码
    :return:
    """
    return GrafanaMangerService.syncHost(host, timeSegmentLabel, username, password)


# 同步修改重要的配置参数
@router.post("/conf/params")
async def modify_primary_conf_params(msHost: Optional[str] = None, mdHost: Optional[str] = None,
                                     dbHost: Optional[str] = None, dbUser: Optional[str] = None,
                                     dbPw: Optional[str] = None, dbName: Optional[str] = None,
                                     grafanaHost: Optional[str] = None, sjzyHost: Optional[str] = None,
                                     schema: Optional[bool] = None, sample: Optional[int] = None,
                                     multiSelf: Optional[bool] = None, clickGap: Optional[int] = None):
    """
    修改MS配置文件参数
    :param msHost:
            MS host
    :param mdHost:
            MD host
    :param dbHost:
            db host
    :param dbUser:
            db 用户名
    :param dbPw:
            db 密码
    :param dbName:
            db 名称
    :param grafanaHost:
            grafana host
    :param sjzyHost:
            数据资源host
    :param schema:
            模式
    :param sample:
            采样
    :param multiSelf:
            是否支持多个设备、测点自相关模型
    :param clickGap:
            点击时间间隔
    :return:
    """
    return ConfigManagerService.update(msHost, mdHost, dbHost, dbUser, dbPw, dbName,
                                       grafanaHost, sjzyHost, schema, sample, multiSelf, clickGap)


# 获取重要的配置参数
@router.get("/conf/getParams")
async def query_primary_conf_params():
    return ConfigManagerService.query()
