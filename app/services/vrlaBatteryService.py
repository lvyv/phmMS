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

business logic层，负责实现电池模型的业务模型。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

import logging
import httpx
import time
import json
from schemas.reqhistory_model import ReqItemCreate
from services.convert.self_relation_util import SelfRelationUtil
from services.main import AppService
from models.dao_reqhistory import RequestHistoryCRUD
from utils.service_result import ServiceResult
from utils.app_exceptions import AppException
from phmconfig import constants as ct


class VRLABatteryService(AppService):
    """
    电池模型业务逻辑服务。
    """

    async def soh(self, devs: list, tags: list, startts: int, endts: int) -> ServiceResult:
        """
        健康指标计算。
        :param devs:
        :param tags:
        :param startts:
        :param endts:
        :return:
        """
        dev_type = ct.DEV_VRLA

        devs.sort()
        tags.sort()

        external_data = {
            'model': dev_type,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            'memo': json.dumps(devs),
            'metrics': json.dumps(tags),
            'startTs': startts,
            'endTs': endts
        }
        item = ReqItemCreate(**external_data)
        soh_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs),
                    "tags": json.dumps(tags),
                    "startts": startts,
                    "endts": endts
                }
                params = {"reqid": soh_item.id}
                r = await client.post(f'{ct.URL_MS_CALL_SOH}', json=payload, params=params)
                logging.debug(r)
                return ServiceResult(r.content)
        except httpx.ConnectTimeout:
            return ServiceResult(AppException.HttpRequestTimeout())

    async def cluster(self, devs: list, tags: list, startts: int, endts: int, displayType: str) -> ServiceResult:
        """
        聚类计算。
        :param devs:
        :param tags:
        :param startts:
        :param endts:
        :return:
        """
        dev_type = ct.DEV_VRLA

        # FIX
        devs.sort()
        tags.sort()

        external_data = {
            'model': dev_type,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            'memo': json.dumps(devs),
            'metrics': json.dumps(tags),
            'displayType': displayType,
            'startTs': startts,
            'endTs': endts
        }
        item = ReqItemCreate(**external_data)
        cluster_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs),
                    "tags": json.dumps(tags),
                    "startts": startts,
                    "endts": endts
                }
                params = {"reqid": cluster_item.id, "displayType": displayType}
                r = await client.post(f'{ct.URL_MS_CALL_CLUSTER}', json=payload, params=params)
                logging.debug(r)
                return ServiceResult(r.content)
        except httpx.ConnectTimeout:
            return ServiceResult(AppException.HttpRequestTimeout())

    async def relation(self, devs: list, tags: list, startts: int, endts: int,
                       leftTag: int, rightTag: int, step: int, unit: int) -> ServiceResult:

        dev_type = ct.DEV_VRLA
        # FIX
        devs.sort()
        tags.sort()

        external_data = {
            'model': dev_type,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            'memo': json.dumps(devs),
            'metrics': json.dumps(tags),
            'displayType': SelfRelationUtil.DISPLAY_SELF_RELATION,
            'startTs': startts,
            'endTs': endts
        }
        item = ReqItemCreate(**external_data)
        cluster_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs),
                    "tags": json.dumps(tags),
                    "startts": startts,
                    "endts": endts
                }
                params = {"reqid": cluster_item.id, "leftTag": leftTag,
                          "rightTag": rightTag, "step": step, "unit": unit}
                r = await client.post(f'{ct.URL_MS_CALL_RELATION}', json=payload, params=params)
                logging.debug(r)
                return ServiceResult(r.content)
        except httpx.ConnectTimeout:
            return ServiceResult(AppException.HttpRequestTimeout())
