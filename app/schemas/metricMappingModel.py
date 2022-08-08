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
from pydantic import BaseModel


class MetricMappingModel(BaseModel):
    metric_code: str    # 测点编码
    metric_name: str    # 测点名称
    metric_alias: str   # 测点别名
    equip_type: str     # 装备类型
    equip_code: str     # 装备编码
    equip_name: str     # 装备名称
    metric_describe: str  # 测点描述
    equip_type_code: str  # 装备类型编码
    metric_unit: str      # 测点单位

    class Config:
        orm_mode = True
