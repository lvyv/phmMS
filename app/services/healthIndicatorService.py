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
from models.dao_cellpack import CellPackCRUD
from services.main import AppService
from utils.service_result import ServiceResult
from services.convert.convertor_factory import ConvertorFactory


class HealthIndicatorService(AppService):
    # 获取健康指标从评估数据表中获取
    def health_indicator(self, clz, code, type) -> ServiceResult:
        devs = code.split(",")
        if type == '0' or 0:
            limit = 1
        else:
            limit = 50
        items = CellPackCRUD(self.db).get_records_by_limit(devs, limit)
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        convertItems = convertor.convertHealthIndicator(items)
        return ServiceResult(convertItems)
