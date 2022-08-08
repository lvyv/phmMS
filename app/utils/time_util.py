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
import time
import calendar
from phmconfig.timeUtils import  TimeUtils


class TimeUtil:

    @staticmethod
    def convert_time_stamp(timeStr):
        # 2022-02-13T22:09:59.457Z
        timeStamp = calendar.timegm(
            time.strptime(timeStr, '%Y-%m-%dT%H:%M:%S.%fZ'))
        return timeStamp * 1000

    @staticmethod
    def convert_time_utc_str(timeStamp):
        # 将linux时间转化为 2022-02-13T22:09:59.000Z
        time_tuple = time.localtime(int(timeStamp / 1000) - 8 * 3600)
        timeStr = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time_tuple)
        return timeStr

    @staticmethod
    def convert_time_utc_8_str(timeStamp):
        return TimeUtils.convert_time_str(timeStamp)
