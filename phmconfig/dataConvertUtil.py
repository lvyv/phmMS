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
import json
import time

from services.convert.cluster_display_util import ClusterDisplayUtil


class DataConvertUtil:
    """
    数据转换
    """
    @staticmethod
    def SOH(reqid, item):
        keys = item.keys()

        eqi = {
            "did": item['did'] if 'did' in keys else "unknown",
            "dclz": "N/A",
            "reqId": reqid,
            "ts": item['ts'] if 'ts' in keys else 0,
        }
        for i in range(39):
            if i < 9:
                key = "M0" + str(i + 1)
            else:
                key = "M" + str(i + 1)
            eqi.update({key: item[key] if key in keys else 0})
        for i in range(1):
            key = "IM" + str(i + 1)
            eqi.update({key: item[key] if key in keys else 0})
        for i in range(5):
            key = "AM" + str(i + 1)
            eqi.update({key: json.dumps(item[key]) if key in keys else "[0]"})
        for i in range(5):
            key = "FM" + str(i + 1)
            eqi.update({key: item[key] if key in keys else 0})
        return eqi

    @staticmethod
    def cluster(reqid, displayType, did,  items):
        eqi = {
            "reqId": reqid,
            "ts": int(time.time() * 1000),
            "name": items[did][0],
            "size": 0,  # items[did][1],
            "color": items[did][2],
            "shape": 0,  # items[did][3],
            "x": items[did][4],
            "y": items[did][5],
            "z": 0  # items[did][6]
        }

        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D]:
            eqi["size"] = items[did][1]

        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D]:
            eqi["shape"] = items[did][3]

        if displayType in [ClusterDisplayUtil.DISPLAY_3D, ClusterDisplayUtil.DISPLAY_AGG3D]:
            eqi["z"] = items[did][6]

        return eqi


