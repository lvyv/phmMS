import json
import httpx
from phmconfig import constants


class DataCenterService:
    # equipName: 装备名称
    # equipCode: 装备编码
    # equipTypeCode: 装备类型编码
    @staticmethod
    def download_zb_metric(equipTypeCode=None, equipCode=None, equipName=None, hasFilter=True):
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
            return DataCenterService.process_zb_metric(dataS, hasFilter)
        return None

    @staticmethod
    def process_zb_metric(data, hasFilter=True):
        mappings = []
        if data is None:
            return None
        result = data["result"]
        for res in result:
            equipCode = res["equipCode"] if "equipCode" in res.keys() else ''
            equipName = res["equipName"] if "equipName" in res.keys() else ''
            equipTypeCode = res["equipTypeCode"] if "equipTypeCode" in res.keys() else ''

            # TODO 过滤空
            if equipTypeCode is '':
                continue

            if hasFilter is True:
                if "measurePoints" in res.keys():
                    for item in res["measurePoints"]:
                        code = item["pointCode"] if "pointCode" in item.keys() else ''
                        name = item["pointName"] if "pointName" in item.keys() else ''
                        unit = item["pointUnit"] if "pointUnit" in item.keys() else ''
                        mappings.append({"equipCode": equipCode, "equipName": equipName, "equipTypeCode": equipTypeCode,
                                         "metricCode": code, "metricName": name, "metricUnit": unit})
            else:
                mappings.append({"equipCode": equipCode, "equipName": equipName, "equipTypeCode": equipTypeCode})
        return mappings

    @staticmethod
    def filter_zb_equip_type_code(mappings):
        tmpDict = {}
        ret = []
        for mapping in mappings:
            if mapping["equipTypeCode"] not in tmpDict.keys():
                tmpDict[mapping["equipTypeCode"]] = mapping
        for key in tmpDict.keys():
            if "metricCode" in tmpDict[key].keys():
                tmpDict[key].pop("metricCode")
            if "metricName" in tmpDict[key].keys():
                tmpDict[key].pop("metricName")
            if "equipCode" in tmpDict[key].keys():
                tmpDict[key].pop("equipCode")
            ret.append(tmpDict[key])
        return ret
