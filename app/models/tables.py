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
from sqlalchemy import Column, Integer, String, FLOAT, INTEGER, BigInteger, Boolean, TEXT
from phmconfig.database import Base, create_tables


class TReqHistory(Base):
    """
    在phmMS收到REST调用时，创建一条记录，保存该异步请求，之后调用phmMD。
    在phmMD被调用启动的工作线程完成耗时计算后，反向回调phmMS，保存原来异步请求的执行结果。
    该表主要字段：
        id: 记录请求号，每次调用都是唯一的；
        model: 记录请求是针对哪个模型；
        status: 该请求的执行状态；
        result: 请求执行的结果。
        requestts: 客户端调用的时间戳。
        settledts: Ai模型执行完成的时间戳。
        memo: 放设备id。
        metrics: 存放设备测点。
    """
    __tablename__ = "xc_req_history"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(TEXT)
    status = Column(TEXT)
    result = Column(TEXT)
    requestts = Column(BigInteger)
    settledts = Column(BigInteger)
    memo = Column(TEXT)
    metrics = Column(TEXT)
    displayType = Column(TEXT)
    startTs = Column(BigInteger)
    endTs = Column(BigInteger)
    params = Column(TEXT)


class TCellPack(Base):
    """
    模型评估表，用于设备存放测量值与部分计算值
    """
    __tablename__ = "xc_cell_pack"
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    # 执行请求ID 关联历史记录表
    reqId = Column(Integer)
    # 时间
    ts = Column(BigInteger)
    # 装备ID
    did = Column(TEXT)
    # 装备类型
    dclz = Column(TEXT)

    # 普通测点   可采集的测点
    M01 = Column(FLOAT)
    M02 = Column(FLOAT)
    M03 = Column(FLOAT)
    M04 = Column(FLOAT)
    M05 = Column(FLOAT)
    M06 = Column(FLOAT)
    M07 = Column(FLOAT)
    M08 = Column(FLOAT)
    M09 = Column(FLOAT)
    M10 = Column(FLOAT)
    M11 = Column(FLOAT)
    M12 = Column(FLOAT)
    M13 = Column(FLOAT)
    M14 = Column(FLOAT)
    M15 = Column(FLOAT)
    M16 = Column(FLOAT)
    M17 = Column(FLOAT)
    M18 = Column(FLOAT)
    M19 = Column(FLOAT)
    M20 = Column(FLOAT)
    M21 = Column(FLOAT)
    M22 = Column(FLOAT)
    M23 = Column(FLOAT)
    M24 = Column(FLOAT)
    M25 = Column(FLOAT)
    M26 = Column(FLOAT)
    M27 = Column(FLOAT)
    M28 = Column(FLOAT)
    M29 = Column(FLOAT)
    M30 = Column(FLOAT)
    M31 = Column(FLOAT)
    M32 = Column(FLOAT)
    M33 = Column(FLOAT)
    M34 = Column(FLOAT)
    M35 = Column(FLOAT)
    M36 = Column(FLOAT)
    M37 = Column(FLOAT)
    M38 = Column(FLOAT)
    M39 = Column(FLOAT)

    # 组测点  eg: # 电池组的环境温度集合,  # 电池单元端电压集合 , # 电池单元容量集合
    AM1 = Column(TEXT)
    AM2 = Column(TEXT)
    AM3 = Column(TEXT)
    AM4 = Column(TEXT)
    AM5 = Column(TEXT)

    # 整型测点 eg: # 健康状态
    IM1 = Column(Integer)

    # 用于计算模型结果存放字段
    FM1 = Column(FLOAT)
    FM2 = Column(FLOAT)
    FM3 = Column(FLOAT)
    FM4 = Column(FLOAT)
    FM5 = Column(FLOAT)


class TCluster(Base):
    """
    聚类计算表，用于存放聚类计算结果
    """
    __tablename__ = "xc_cluster"
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    # 时间
    ts = Column(BigInteger)
    # 执行请求ID 关联历史记录表
    reqId = Column(Integer)
    # x 轴坐标
    x = Column(FLOAT)
    # y 轴坐标
    y = Column(FLOAT)
    # z 轴坐标
    z = Column(FLOAT)
    # 颜色值 eg: "red", "green", "yellow", "blue", "gray","black", "orange"
    color = Column(TEXT)
    # 大小
    size = Column(FLOAT)
    # 形状 eg: "circle", "star","square", "cross", "diamond"
    shape = Column(TEXT)
    # 装备ID
    name = Column(TEXT)


class TSelfRelation(Base):
    """
    自相关表，用于存放自相关计算值
    """
    __tablename__ = "xc_self_relation"
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    # 计算时间
    ts = Column(BigInteger)
    # 请求ID
    reqId = Column(Integer)
    # lag
    lag = Column(Integer)
    # 值
    value = Column(FLOAT)
    # 设备ID+测点
    own_key = Column(TEXT)


class TMetricMapping(Base):
    """
    测点映射表
    """
    __tablename__ = "xc_metric_mapping"
    id = Column(Integer, primary_key=True, index=True)
    # 测点编码      ignore
    metric_code = Column(TEXT)
    # 测点名称
    metric_name = Column(TEXT)
    # 测点别名
    metric_alias = Column(TEXT)
    # 装备编码      ignore
    equip_code = Column(TEXT)
    # 装备名称      ignore
    equip_name = Column(TEXT)
    # 装备类型
    equip_type = Column(TEXT)
    # 装备类型编码
    equip_type_code = Column(TEXT)
    # 描述   ignore
    metric_describe = Column(TEXT)
    # 测点类型
    metric_unit = Column(TEXT)


class TEquipTypeMapping(Base):
    """
    装备编码映射
    """
    __tablename__ = "xc_equip_type_mapping"
    id = Column(Integer, primary_key=True, index=True)
    # 装备类型编码
    equip_type_code = Column(TEXT)
    # 装备类型
    equip_type = Column(TEXT)


# create all tables
TABLES = create_tables()
