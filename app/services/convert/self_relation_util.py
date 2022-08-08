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
from phmconfig.timeUtils import TimeUtils
from utils.payload_util import PayloadUtil


class SelfRelationUtil:
    DISPLAY_SELF_RELATION = "SELF_RELATION"
    DISPLAY_SELF_RELATION_POLYLINE = "SELF_POLYLINE"

    @staticmethod
    def get_use_metrics(displayType):
        values = {
            "SELF_RELATION": ["lag", "value"]
        }
        return values.get(displayType, None)

    @staticmethod
    def get_metric_value(item, metric):
        values = {
            "lag": item.lag,
            "value": item.value,
        }
        return values.get(metric, None)

    @staticmethod
    def get_metric_type(key):
        if key in ["ts"]:
            return "time"
        return "number"

    @staticmethod
    def getTagInfoByPayload(payload):
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)
        return start, end

    @staticmethod
    def getTagInfoByTime(subTime):
        subTimeLong = TimeUtils.convert_time_stamp(subTime)
        return subTimeLong

