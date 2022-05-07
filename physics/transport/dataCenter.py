import httpx
from phmconfig import constants


# 从数据资源下载下载装备数据
def download_zb_data(devs, metrics, start, end):
    with httpx.Client(timeout=None, verify=False) as client:
        r = client.post(constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbData", params={"devs": devs, "metrics": metrics, "start": start, "end": end})
        dataS = r.json()
        return dataS
    return None


# equipName: 装备名称
# equipCode: 装备编码
# equipTypeCode: 装备类型编码
def download_zb_metric_from(equipName, equipCode, equipTypeCode):
    with httpx.Client(timeout=None, verify=False) as client:
        url = constants.API_QUERY_EQUIP_INFO_WITH_MEASURE_POINT
        r = client.post(url,
                        params={"equipName": equipName, "equipCode": equipCode, "equipTypeCode": equipTypeCode})
        dataS = r.json()
        return dataS
    return None


# metricName: 测点编号， 多个测点之间采用逗号隔开
# startTime：查询开始时间  格式yyyy-MM-dd HH:mm:ss
# endTime: 查询结束时间  格式 yyyy-MM-dd HH:mm:ss
# interval: 数据抽取间隔  格式 [数字][M|H|D]
def download_zb_history_data_from(metricName, startTime, endTime, interval):
    with httpx.Client(timeout=None, verify=False) as client:
        url = constants.API_QUERY_HISTORY_DATA
        r = client.post(url,
                        params={"metricName": metricName, "startTime": startTime, "endTime": endTime,
                                "interval": interval})
        dataS = r.json()
        return dataS
    return None
