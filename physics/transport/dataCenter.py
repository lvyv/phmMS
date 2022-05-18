import json

import httpx
from phmconfig import constants

# 从数据资源下载下载装备数据
from phmconfig.timeUtils import TimeUtils


# 模拟数据  设备编码， 测点名称 ， 开始时间， 结束时间
def download_zb_data(devs, metrics, start, end):
    with httpx.Client(timeout=None, verify=False) as client:
        r = client.post(constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbData2",
                        params={"devs": devs, "metrics": metrics, "start": start, "end": end})
        dataS = r.json()
        return dataS
    return None


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
