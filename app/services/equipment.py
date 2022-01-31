#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

"""
=========================
business logic layer
=========================

business logic层，负责实现客户端请求的结果入库和查询。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from services.main import AppService
from models.dao_equipment import EquipmentCRUD
from utils.service_result import ServiceResult
import time
# from utils.app_exceptions import AppException


class EquipmentService(AppService):
    def create_items(self, pi, counts=500000) -> ServiceResult:
        equipment_item = None
        pi.devclass = 'BATTERY'
        for ii in range(counts):
            pi.ts = int(time.time()*1000)
            pi.did = f'd{ii % 40}'
            pi.dis_dischargecycles = ii
            equipment_item = EquipmentCRUD(self.db).create_record(pi)
        return ServiceResult(equipment_item)

    def create_item(self, pi) -> ServiceResult:
        equipment_item = EquipmentCRUD(self.db).create_record(pi)
        return ServiceResult(equipment_item)

    def get_item(self, pi) -> ServiceResult:
        equipment_item = EquipmentCRUD(self.db).get_record(pi)
        return ServiceResult(equipment_item)

    def get_items(self, pi, sts, ets) -> ServiceResult:
        equipment_items = EquipmentCRUD(self.db).get_records(pi, sts, ets)
        return ServiceResult(equipment_items)
