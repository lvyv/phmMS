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
class ClusterDisplayUtil:
    """
    聚类模型类型
    """
    DISPLAY_SCATTER = "SCATTER"
    DISPLAY_POLYLINE = "POLYLINE"
    DISPLAY_2D = "2D"
    DISPLAY_3D = "3D"
    DISPLAY_AGG2D = "AGG2D"
    DISPLAY_AGG3D = "AGG3D"

    @staticmethod
    def get_use_metrics(displayType):
        """
        通过模型类型获取测点
        :param displayType:
                模型类型
        :return:
        """
        values = {
            "SCATTER": ["ts", "did"],
            "2D": ["x", "y", "color", "size", "shape", "name"],
            "3D": ["x", "y", "z", "color", "size", "shape", "name"],
            "POLYLINE": ["ts"],
            "AGG2D": ["x", "y", "color", "shape", "name"],
            "AGG3D": ["x", "y", "z", "color", "name"]
        }
        return values.get(displayType, None)

    @staticmethod
    def get_metric_value(item, metric):
        """
        获取测点的值
        :param item:
                对象
        :param metric:
                测点
        :return:
        """
        values = {
            "x": item.x,
            "y": item.y,
            "color": item.color,
            "shape": item.shape,
            "name": item.name
        }
        if hasattr(item, "z") is True:
            values["z"] = item.z
        if hasattr(item, "size") is True:
            values["size"] = item.size

        return values.get(metric, None)

    @staticmethod
    def get_metric_type(key):
        if key in ["ts"]:
            return "time"
        if key in ["color", "shape", "name"]:
            return "string"
        return "number"
