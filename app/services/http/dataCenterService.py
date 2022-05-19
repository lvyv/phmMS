import json
import httpx
from phmconfig import constants


class DataCenterService:
    # equipName: 装备名称
    # equipCode: 装备编码
    # equipTypeCode: 装备类型编码
    @staticmethod
    def download_zb_metric(equipTypeCode=None, equipCode=None, equipName=None):
        with httpx.Client(timeout=None, verify=False) as client:
            if constants.MOCK_ZB_DATA is True or constants.MOCK_ZB_DATA is "true":
                url = constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbMetric"
            else:
                url = constants.API_QUERY_EQUIP_INFO_WITH_MEASURE_POINT
            params = {}
            if equipTypeCode is not None:
                params["equipTypeCode"] = equipTypeCode
            if equipCode is not None:
                params["equipCode"] = equipCode
            if equipName is not None:
                params["equipName"] = equipName
            if len(params.keys()) <= 0:
                r = client.post(url)
            else:
                r = client.post(url, params=params)
            dataS = r.json()
            return DataCenterService.process_zb_metric(dataS)
        return None

    @staticmethod
    def process_zb_metric(data):
        mappings = []
        if data is None:
            return None
        equipCode = data["result"]["equipCode"]
        equipName = data["result"]["equipName"]
        equipTypeCode = data["result"]["equipTypeCode"]
        for item in data["result"]["measurePoints"]:
            code = item["pointCode"]
            name = item["pointName"]
            mappings.append({"equipCode": equipCode, "equipName": equipName, "equipTypeCode": equipTypeCode,
                             "metricCode": code, "metricName": name})
        return mappings
