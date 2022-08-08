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
class PublicModelValidate:
    @staticmethod
    def support(equipCode: str, metrics: str):
        if equipCode is '' or metrics is '':
            return False, '', ''
        devs = list(set(filter(None, equipCode.split(","))))
        metrics = list(set(filter(None, metrics.split(","))))
        if len(devs) == 0 or len(metrics) == 0:
            return False, '', ''
        return True, ",".join(dev for dev in devs), ",".join(metric for metric in metrics)
