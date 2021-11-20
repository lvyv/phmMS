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
data access layer
=========================

data access层，负责处理模型调用的历史记录。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from services.main import AppCRUD
from models.tables import TEquipment
from schemas.equipment import EquipmentItemCreate


class EquipmentCRUD(AppCRUD):
    """
    电池模型请求数据访问。
    """

    def create_record(self, item: EquipmentItemCreate) -> TEquipment:
        reqdao = TEquipment(ts=item.ts,  # 主键
                            id=item.id,
                            devclass=item.devclass,
                            dis_voltage=item.dis_voltage,
                            dis_current=item.dis_current,
                            dis_resistance=item.dis_resistance,
                            dis_temperature=item.dis_temperature,
                            dis_dischargecycles=item.dis_dischargecycles,
                            chg_voltage=item.chg_voltage,
                            chg_current=item.chg_current,
                            chg_resistance=item.chg_resistance,
                            chg_temperature=item.chg_temperature,
                            chg_dischargecycles=item.chg_dischargecycles)
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao
