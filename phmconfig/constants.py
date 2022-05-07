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
basic phmconfig module
=========================

定义健康管理模型的各种公共配置。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from phmconfig.config import ConfigSet

cfg = ConfigSet.get_cfg()

# --------------------- MS -------------------------------------
# phmMS启动的地址、端口、证书等
PHMMS_HOST = cfg['phmms_host']
PHMMS_PORT = cfg['phmms_port']
PHMMS_KEY = cfg['phmms_key']
PHMMS_CER = cfg['phmms_cer']

# ------------------------------------ MD -----------------
# phmMD启动的地址、端口、证书等
PHMMD_HOST = cfg['phmmd_host']
PHMMD_PORT = cfg['phmmd_port']
PHMMD_KEY = cfg['phmmd_key']
PHMMD_CER = cfg['phmmd_cer']

# ----------------------------- DB -----------------------

# 数据库地址
PHM_DATABASE_URL = cfg['datasource_url']

#  --------------------------- COMMON -------------------------
# 所有后端的科学计算模型，phmMD类型
DEV_VRLA = 'vrla'
# 各种状态常量
REQ_STATUS_PENDING = 'pending'
REQ_STATUS_SETTLED = 'settled'
# 后台ai模型的地址
REST_REQUEST_TIMEOUT = 10

# ------------------------- api ------------------------------

# prefix
PHMMS_CONTAINER_NAME = cfg["phmms_container_name"]
PHMMS_URL_PREFIX = "https://" + PHMMS_CONTAINER_NAME + ":" + str(PHMMS_PORT)
# 写评估数据
URL_MD_WRITE_EVAL = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeEval"
# 写健康指标URL地址
URL_MS_WRITE_HEALTH_INDICATOR = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeHealthIndicator"
# 写聚类数据
URL_MD_WRITE_CLUSTER = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeCluster"
# 写自相关数据
URL_MD_WRITE_SELF_RELATION = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeRelation"
# 写更新历史请求记录
URL_MD_WRITE_REQ_HISTORY = PHMMS_URL_PREFIX + "/api/v1/reqhistory/item"

# prefix
PHMMD_CONTAINER_NAME = cfg["phmmd_container_name"]
PHMMD_URL_PREFIX = "https://" + PHMMD_CONTAINER_NAME + ":" + str(PHMMD_PORT)
# 调用评估
URL_MS_CALL_SOH = PHMMD_URL_PREFIX + "/api/v1/soh"
# 调用聚类
URL_MS_CALL_CLUSTER = PHMMD_URL_PREFIX + "/api/v1/cluster"
# 调用自相关
URL_MS_CALL_RELATION = PHMMD_URL_PREFIX + "/api/v1/relation"


# 数据资源
URL_SJZY_API_PREFIX = cfg["url_sjzy_host"]
# 从数据资源获取装备所有测点
API_QUERY_EQUIP_INFO_WITH_MEASURE_POINT = URL_SJZY_API_PREFIX + "/api/equip/query_info_with_measure_point"
# 从数据资源获取装备的测点数据
API_QUERY_HISTORY_DATA = URL_SJZY_API_PREFIX + "/api/devices/query_history_data"

