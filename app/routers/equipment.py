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
controller layer
=========================

controller层，负责equipment数据的填入.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from fastapi import APIRouter, Depends
from services.equipment import EquipmentService
from schemas.equipment import EquipmentItem, EquipmentItemCreate
from utils.service_result import handle_result
from phmconfig.database import get_db

router = APIRouter(
    prefix="/api/v1/equipment",
    tags=["基础微服务"],
    responses={404: {"description": "Not found"}},
)


@router.post("/item/{counts}", response_model=EquipmentItem)
async def create_item(item: EquipmentItemCreate, db: get_db = Depends(), counts: int = 0):
    so = EquipmentService(db)
    result = so.create_items(item, counts)
    return handle_result(result)
