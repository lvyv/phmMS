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
import calendar
import time
from phmconfig import constants


class TimeUtils:
    @staticmethod
    def convert_time_str(timestamp):
        time_tuple = time.localtime(timestamp / 1000)
        bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        # print("北京时间:", bj_time)
        return bj_time

    @staticmethod
    def get_time_interval(start, end):
        """
        计算时间间隔
        :param start:
        :param end:
        :return:
        """
        diff = int(end / 1000 - start / 1000)
        maxPoints = constants.EQUIP_DATA_MAX_POINT
        interval = int(diff / maxPoints)
        if interval > 24 * 60 * 60:
            gap = int(interval / (24 * 60 * 60))
            gap = str(gap) + "D"
        elif interval > 60 * 60:
            gap = int(interval / (60 * 60))
            gap = str(gap) + "H"
        elif interval > 60:
            gap = int(interval / 60)
            gap = str(gap) + "M"
        else:
            if constants.MOCK_ZB_DATA is True:
                gap = int((interval / 60) * 10) / 10
                if gap == 0.0:
                    gap = 0.05
                gap = str(gap) + "M"
            else:
                gap = None
        return gap

    @staticmethod
    def convert_time_stamp(timeStr):
        # 2022-02-13 22:09:59
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp * 1000

    @staticmethod
    def convert_time_stamp_utc(timeStr):
        # 2022-02-13 22:09:59 + 8H
        timeStamp = calendar.timegm(
            time.strptime(timeStr, '%Y-%m-%d %H:%M:%S'))
        return timeStamp * 1000
