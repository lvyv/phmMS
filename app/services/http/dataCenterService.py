import json
import httpx
from phmconfig import constants


class DataCenterService:
    # equipName: 装备名称
    # equipCode: 装备编码
    # equipTypeCode: 装备类型编码
    @staticmethod
    def download_zb_type_code():
        with httpx.Client(timeout=None, verify=False) as client:
            if constants.MOCK_ZB_DATA is True or constants.MOCK_ZB_DATA is "true":
                url = constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbMetric"
            else:
                url = constants.API_QUERY_EQUIP_INFO_WITH_MEASURE_POINT
            r = client.post(url)
            dataS = r.json()
            return DataCenterService._process_zb_metric(dataS)
        return None

    @staticmethod
    def _process_zb_metric(data):
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

            if "measurePoints" in res.keys():
                for item in res["measurePoints"]:
                    code = item["pointCode"] if "pointCode" in item.keys() else ''
                    name = item["pointName"] if "pointName" in item.keys() else ''
                    unit = item["pointUnit"] if "pointUnit" in item.keys() else ''
                    mappings.append({"equipCode": equipCode, "equipName": equipName, "equipTypeCode": equipTypeCode,
                                     "metricCode": code, "metricName": name, "metricUnit": unit})
        return mappings

    @staticmethod
    def filter_zb_equip_type_code(mappings):
        tmpDict = {}
        ret = []
        for mapping in mappings:
            if mapping["equipTypeCode"] not in tmpDict.keys():
                tmpDict[mapping["equipTypeCode"]] = mapping
        for key in tmpDict.keys():
            if "equipName" in tmpDict[key].keys():
                tmpDict[key].pop("equipName")
            if "metricCode" in tmpDict[key].keys():
                tmpDict[key].pop("metricCode")
            if "metricName" in tmpDict[key].keys():
                tmpDict[key].pop("metricName")
            if "equipCode" in tmpDict[key].keys():
                tmpDict[key].pop("equipCode")
            if "metricUnit" in tmpDict[key].keys():
                tmpDict[key].pop("metricUnit")
            ret.append(tmpDict[key])
        return ret

    # 新增查询装备测点接口使用
    @staticmethod
    def download_zb_metric_by_type_code(equipTypeCode: str):
        with httpx.Client(timeout=None, verify=False) as client:
            if constants.MOCK_ZB_DATA is True or constants.MOCK_ZB_DATA is "true":
                url = constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbMetricByTypeCode"
            else:
                url = constants.API_QUERY_MEASUSRE_POINT_BY_EQUIP_TYPE_CODE
            params = {"equipTypeCode": equipTypeCode}
            r = client.get(url, params=params)
            dataS = r.json()
            return DataCenterService.parse_zb_metric_by_type_code(equipTypeCode, dataS)
        return None

    @staticmethod
    def parse_zb_metric_by_type_code(equipTypeCode: str, data):
        mappings = []
        if data is None:
            return None
        result = data["result"]
        for res in result["data"]:
            mappings.append({"equipTypeCode": equipTypeCode, "metricName": res["pointName"], "metricUnit": res["unit"]})
        return mappings
