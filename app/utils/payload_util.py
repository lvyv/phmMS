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
from utils.time_util import TimeUtil


class PayloadUtil:

    @staticmethod
    def check_relative_time_valid(payload):
        try:
            start = payload["rangeRaw"]["from"]
            end = payload["rangeRaw"]["to"]
            if "now" in start or "now" in end:
                return False
        except Exception as e:
            # print(e)
            return True


    @staticmethod
    def get_start_time(payload):
        start = TimeUtil.convert_time_stamp(payload["range"]["from"])
        return start

    @staticmethod
    def get_end_time(payload):
        end = TimeUtil.convert_time_stamp(payload["range"]["to"])
        return end

    @staticmethod
    def get_interval_ms(payload):
        return payload["intervalMs"]

    @staticmethod
    def get_limit(payload):
        return payload["maxDataPoints"]

    @staticmethod
    def get_time_zone(payload):
        return payload["timezone"]
