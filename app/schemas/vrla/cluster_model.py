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
from schemas.time_model import TimeModel


class ClusterModel(TimeModel):
    reqId: int  # 执行请求ID 关联历史记录表
    x: float  # x 轴坐标
    y: float  # y 轴坐标
    z: float  # z 轴坐标
    color: str  # 颜色值 eg: "red", "green", "yellow", "blue", "gray","black", "orange"
    size: float  # 大小
    shape: str  # 形状 eg: "circle", "star","square", "cross", "diamond"
    name: str  # 装备ID

    class Config:
        orm_mode = True
