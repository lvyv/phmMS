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

    @staticmethod
    def checkReqValid(devs: list, tags: list):
        """
        参数合法性校验
        :param devs:
        :param tags:
        :return:
        """
        if len(devs) == 0 or len(tags) == 0 or devs == [""] or tags == [""]:
            logging.info("任务调度时，输入的参数非法。输入设备编码为空或者测点名称为空")
            return False
        return True

    async def soh(self, equipTypeCode: str, devs: list, tags: list, startts: int, endts: int,
                  displayType: str) -> ServiceResult:
        """
        装备SOH模型调度
        :param equipTypeCode:
        :param devs:
        :param tags:
        :param startts:
        :param endts:
        :param displayType:
        :return:
        """

        if VRLABatteryService.checkReqValid(devs, tags) is False:
            return ServiceResult("任务调度时，输入的参数非法。输入设备编码为空或者测点名称为空")

        devs.sort()
        tags.sort()

        external_data = {
            'model': equipTypeCode,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            'memo': json.dumps(devs, ensure_ascii=False),
            'metrics': json.dumps(tags, ensure_ascii=False),
            'startTs': startts,
            'endTs': endts,
            'displayType': displayType,
            'params': ''
        }
        item = ReqItemCreate(**external_data)
        soh_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs, ensure_ascii=False),
                    "tags": json.dumps(tags, ensure_ascii=False),
                    "startts": startts,
                    "endts": endts,
                    "equipTypeCode": equipTypeCode
                }
                params = {"reqid": soh_item.id}
                r = await client.post(f'{ct.URL_MS_CALL_SOH}', json=payload, params=params)
                logging.debug(r)
                return ServiceResult(r.content)
        except httpx.ConnectTimeout:
            return ServiceResult(AppException.HttpRequestTimeout())

    async def cluster(self, equipTypeCode: str, devs: list, tags: list, startts: int, endts: int,
                      displayType: str) -> ServiceResult:
        """
        聚类模型调度
        :param equipTypeCode:
        :param devs:
        :param tags:
        :param startts:
        :param endts:
        :param displayType:
        :return:
        """

        if VRLABatteryService.checkReqValid(devs, tags) is False:
            return ServiceResult("任务调度时，输入的参数非法。输入设备编码为空或者测点名称为空")

        devs.sort()
        tags.sort()

        external_data = {
            'model': equipTypeCode,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            'memo': json.dumps(devs, ensure_ascii=False),
            'metrics': json.dumps(tags, ensure_ascii=False),
            'displayType': displayType,
            'startTs': startts,
            'endTs': endts,
            'params': ''
        }
        item = ReqItemCreate(**external_data)
        cluster_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs, ensure_ascii=False),
                    "tags": json.dumps(tags, ensure_ascii=False),
                    "startts": startts,
                    "endts": endts,
                    "equipTypeCode": equipTypeCode
                }
                params = {"reqid": cluster_item.id, "displayType": displayType}
                r = await client.post(f'{ct.URL_MS_CALL_CLUSTER}', json=payload, params=params)
                logging.debug(r)
                return ServiceResult(r.content)
        except httpx.ConnectTimeout:
            return ServiceResult(AppException.HttpRequestTimeout())

    async def relation(self, equipTypeCode: str, devs: list, tags: list, startts: int, endts: int,
                       subFrom: int, subTo: int) -> ServiceResult:

        """
        自相关模型调度
        :param equipTypeCode:
        :param devs:
        :param tags:
        :param startts:
        :param endts:
        :param subFrom:
        :param subTo:
        :return:
        """

        if VRLABatteryService.checkReqValid(devs, tags) is False:
            return ServiceResult("任务调度时，输入的参数非法。输入设备编码为空或者测点名称为空")

        devs.sort()
        tags.sort()

        external_data = {
            'model': equipTypeCode,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            'memo': json.dumps(devs, ensure_ascii=False),
            'metrics': json.dumps(tags, ensure_ascii=False),
            'displayType': SelfRelationUtil.DISPLAY_SELF_RELATION,
            'startTs': startts,
            'endTs': endts,
            'params': json.dumps({"subFrom": subFrom, "subTo": subTo}, ensure_ascii=False)
        }
        item = ReqItemCreate(**external_data)
        cluster_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs, ensure_ascii=False),
                    "tags": json.dumps(tags, ensure_ascii=False),
                    "startts": startts,
                    "endts": endts,
                    "equipTypeCode": equipTypeCode
                }
                params = {"reqid": cluster_item.id, "subFrom": subFrom, "subTo": subTo}
                r = await client.post(f'{ct.URL_MS_CALL_RELATION}', json=payload, params=params)
                logging.debug(r)
                return ServiceResult(r.content)
        except httpx.ConnectTimeout:
            return ServiceResult(AppException.HttpRequestTimeout())
