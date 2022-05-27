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

    async def soh(self, devs: list, tags: list, startts: int, endts: int, displayType: str) -> ServiceResult:
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
            'memo': json.dumps(devs, ensure_ascii=False),
            'metrics': json.dumps(tags, ensure_ascii=False),
            'startTs': startts,
            'endTs': endts,
            'displayType': displayType
        }
        item = ReqItemCreate(**external_data)
        soh_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs, ensure_ascii=False),
                    "tags": json.dumps(tags, ensure_ascii=False),
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
            'memo': json.dumps(devs, ensure_ascii=False),
            'metrics': json.dumps(tags, ensure_ascii=False),
            'displayType': displayType,
            'startTs': startts,
            'endTs': endts
        }
        item = ReqItemCreate(**external_data)
        cluster_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs, ensure_ascii=False),
                    "tags": json.dumps(tags, ensure_ascii=False),
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
            'memo': json.dumps(devs, ensure_ascii=False),
            'metrics': json.dumps(tags, ensure_ascii=False),
            'displayType': SelfRelationUtil.DISPLAY_SELF_RELATION,
            'startTs': startts,
            'endTs': endts
        }
        item = ReqItemCreate(**external_data)
        cluster_item = RequestHistoryCRUD(self.db).create_record(item)
        try:
            async with httpx.AsyncClient(timeout=ct.REST_REQUEST_TIMEOUT, verify=False) as client:
                payload = {
                    "devices": json.dumps(devs, ensure_ascii=False),
                    "tags": json.dumps(tags, ensure_ascii=False),
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
