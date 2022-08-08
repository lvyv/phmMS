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
import database
from services.metricMappingService import MetricMappingService


class MetricMappingUtils:

    def __init__(self, equipTypeCode):
        db = database.SessionLocal()
        so = MetricMappingService(db)
        self.items = so.get_all_mapping_by_equip_type_code(equipTypeCode)

    def get_own_metrics(self, metrics):
        ret = []
        for metric in metrics:
            if metric in ["ts"]:
                ret.append("ts")
            else:
                if metric in self.items.keys():
                    ret.append(self.items[metric])
                else:
                    ret.append(metric)
        return ret

    def get_own_metric(self, metric):
        if metric in ["ts"]:
            return "ts"
        if metric in self.items.keys():
            return self.items[metric]
        else:
            return metric
