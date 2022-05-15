import json

import httpx
from phmconfig import constants

# 从数据资源下载下载装备数据
from timeUtils import TimeUtils


# 模拟数据
def download_zb_data(devs, metrics, start, end):
    with httpx.Client(timeout=None, verify=False) as client:
        r = client.post(constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbData2",
                        params={"devs": devs, "metrics": metrics, "start": start, "end": end})
        dataS = r.json()
        return dataS
    return None


# equipName: 装备名称
# equipCode: 装备编码
# equipTypeCode: 装备类型编码
def download_zb_metric_from(equipCode, equipName=None, equipTypeCode=None):
    with httpx.Client(timeout=None, verify=False) as client:
        # url = constants.API_QUERY_EQUIP_INFO_WITH_MEASURE_POINT
        url = constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbMetric"
        if equipName is None and equipTypeCode is None:
            params = {"equipCode": equipCode}
        elif equipName is None:
            params = {"equipCode": equipCode, "equipTypeCode": equipTypeCode}
        elif equipTypeCode is None:
            params = {"equipName": equipName, "equipCode": equipCode}
        else:
            params = {"equipName": equipName, "equipCode": equipCode, "equipTypeCode": equipTypeCode}
        r = client.post(url, params=params)
        dataS = r.json()
        return dataS
    return None


# result
#  delFlag | updateBy | updateTime | createBy | createTime | useDate | price | durableYears | personCharge | model \
#  | manufactureNation | nameplateDate | batch | equipTypeCode | constructionTtem | equipName | equipCode | remark \
#  | measurePoints
#  measurePoints: 测点数据
#  pointCode | pointName | protocol | dataType | description

#  需要处理的数据 result.equipName result.equipCode result.equipTypeCode
#  result.measurePoints[i].pointCode  result.measurePoints[i].pointName

def process_zb_metric_from(data):
    if data is None:
        return None
    equipCode = data["result"]["equipCode"]
    equipName = data["result"]["equipName"]
    equipTypeCode = data["result"]["equipTypeCode"]
    for item in data["result"]["measurePoints"]:
        code = item["pointCode"]
        name = item["pointName"]
    pass


#  ######################################

# metricName: 测点编号， 多个测点之间采用逗号隔开
# startTime：查询开始时间  格式yyyy-MM-dd HH:mm:ss
# endTime: 查询结束时间  格式 yyyy-MM-dd HH:mm:ss
# interval: 数据抽取间隔  格式 [数字][M|H|D]
def download_zb_history_data_from(metricName, startTime, endTime, interval):
    with httpx.Client(timeout=None, verify=False) as client:
        # url = constants.API_QUERY_HISTORY_DATA
        url = constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbData"
        r = client.post(url,
                        params={"metricName": metricName, "startTime": startTime, "endTime": endTime,
                                "interval": interval})
        dataS = r.json()
        return dataS
    return None


# 返回数据
#  apiVersion | message | requestId | code | result
#  code : success->成功  other->异常
#  result: 数据列表
#  metric_name | metric_value | timestamp | quality

# 2022-05-10 16:14:52  -> 1652170492000  | 2022-05-11 16:14:52 -> 1652256892000

def process_zb_history_data_from(data):
    if data is None:
        return None
    code = data["code"]
    if code == "success":
        for item in data["result"]:
            name = item["metric_name"]
            value = item["metric_value"]
            timestamp = item["timestamp"]
    pass


# devs:设备编号
# metrics: 测点名称  注意不是测点编码
# start end : 时间戳ms
def download_zb_data_inner(devs, metrics, start, end):
    devices = json.loads(devs)
    measurePoints = json.loads(metrics)
    startStr = TimeUtils.convert_time_str(start)
    endStr = TimeUtils.convert_time_str(end)
    interval = TimeUtils.get_time_interval(start, end)
    metricNames = ",".join(item for item in measurePoints)
    datas = download_zb_history_data_from(metricNames, startStr, endStr, interval)
    retDatas = convert_2D_3D_data(datas)
    # convert_2DAgg_data(datas)
    return retDatas


# ---聚类的数据结构
# 2D 3D
# 设备1  时间戳  测点1 测点2
# 设备1  时间戳  测点1 测点2
# 设备2  时间戳  测点1 测点2
def convert_2D_3D_data(data):
    if data is None:
        return None
    code = data["code"]
    tmpDic = {}
    dataList = []
    if code == "success":
        for item in data["result"]:
            name = item["metric_name"]
            value = item["metric_value"]
            timestamp = item["timestamp"]
            if timestamp in tmpDic.keys():
                tmpDic[timestamp].append(value)
            else:
                tmpDic[timestamp] = [value]
    ret = {"dev1": {}}
    for key in tmpDic.keys():
        dataList.append(tmpDic[key])
        ret["dev1"][key] = tmpDic[key]
    return ret


# 时序聚类 （2D）
# 设备1 时间段 测点1 测点2
# 设备2 时间段 测点1 测点2
def convert_2DAgg_data(data):
    if data is None:
        return None
    code = data["code"]
    tmpDic = {}
    dataList = []
    if code == "success":
        for item in data["result"]:
            name = item["metric_name"]
            value = item["metric_value"]
            timestamp = item["timestamp"]
            if name in tmpDic.keys():
                tmpDic[name].append(value)
            else:
                tmpDic[name] = [value]
    ret = {"dev1": {}}
    for key in tmpDic.keys():
        dataList.append(tmpDic[key])
        ret["dev1"][key] = tmpDic[key]
    return ret


# 聚类时间演化 （3D） x戳表示时间  2D聚类
# 设备1  时间戳  测点1 测点2
# 设备1  时间戳  测点1 测点2
# 设备2  时间戳  测点1 测点2
