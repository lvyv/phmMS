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
import json

import httpx
from phmconfig import constants

# 从数据资源下载下载装备数据
from phmconfig.timeUtils import TimeUtils


#   设备编码， 测点名称 ， 开始时间， 结束时间
def download_zb_data(devs, metrics, start, end):
    return download_zb_real_data(devs, metrics, start, end)


#  ######################################
# equipCode:  装备编码，  多个装备之间用逗号隔开
# metricName: 测点名称， 多个测点之间采用逗号隔开
# startTime：查询开始时间  格式yyyy-MM-dd HH:mm:ss
# endTime: 查询结束时间  格式 yyyy-MM-dd HH:mm:ss
# interval: 数据抽取间隔  格式 [数字][M|H|D]
def download_zb_history_data_from(equipCode, metricName, startTime, endTime, interval):
    with httpx.Client(timeout=constants.REST_REQUEST_TIMEOUT, verify=False) as client:
        if constants.MOCK_ZB_DATA is True or constants.MOCK_ZB_DATA is "true":
            url = constants.PHMMD_URL_PREFIX + "/api/v1/mock/zbData"
        else:
            url = constants.API_QUERY_HISTORY_DATA

        params = {"equipCode": equipCode, "metricName": metricName,
                  "startTime": startTime, "endTime": endTime}
        if interval is not None:
            params.update({"interval": interval})

        r = client.post(url, params=params)
        dataS = r.json()
        return dataS
    return None


# devs:设备编号
# metrics: 测点名称  注意不是测点编码
# start end : 时间戳ms
def download_zb_real_data(devs, metrics, start, end):
    devices = json.loads(devs)
    measurePoints = json.loads(metrics)
    startStr = TimeUtils.convert_time_str(start)
    endStr = TimeUtils.convert_time_str(end)
    interval = TimeUtils.get_time_interval(start, end)
    equipCodes = ",".join(item for item in devices)
    metricNames = ",".join(item for item in measurePoints)
    data = download_zb_history_data_from(equipCodes, metricNames, startStr, endStr, interval)
    return data


# 返回数据
#  apiVersion | message | requestId | code | result
#  code : success->成功  other->异常
#  result: 数据列表
#  metric_name | metric_value | timestamp | quality

# 2022-05-10 16:14:52  -> 1652170492000  | 2022-05-11 16:14:52 -> 1652256892000


# ---聚类的数据结构
# 2D 3D
# 设备1  时间戳  测点1 测点2
# 设备1  时间戳  测点1 测点2
# 设备2  时间戳  测点1 测点2

# 聚类时间演化 （3D） x戳表示时间  2D聚类
# 设备1  时间戳  测点1 测点2
# 设备1  时间戳  测点1 测点2
# 设备2  时间戳  测点1 测点2

# 生成2D,3D, 聚类时间演化数据格式
def process_zb_history_data_2d_3d_agg3d(data):
    if data is None:
        return None, None, None
    code = data["code"]
    if code == "success":
        dataList = []
        ageList = []
        devList = []
        tmpDic = {}
        for item in data["result"]:
            equipCode = item["equipCode"]  # 装备编码
            equipName = item["equipName"]  # 装备名称
            equipData = item["equipData"]  # 装备数据
            maxLen = 0
            for ed in equipData:
                metricName = ed["metricName"]  # 测点名称
                metricCode = ed["metricCode"]  # 测点编码
                metricData = ed["metricData"]  # 测点数据
                maxLen = max(maxLen, len(metricData))
                for i, md in enumerate(metricData):
                    devKey = equipName + str(i)
                    timestamp = md["timestamp"]  # 时间戳
                    metricValue = md["metricValue"]  # 测点值
                    if devKey in tmpDic.keys():
                        tmpDic[devKey].append(metricValue)
                    else:
                        tmpDic[devKey] = [metricValue]
            ageList.append(maxLen)
            devList.append(equipName)

        for key in tmpDic.keys():
            dataList.append(tmpDic[key])
        return dataList, ageList, devList
    else:
        return None, None, None


# 时序聚类 （2D）
# 设备1 时间段 测点1 测点2
# 设备2 时间段 测点1 测点2

# 生成时序聚类格式数据
def process_zb_history_data_agg2d(data):
    if data is None:
        return None, None, None
    code = data["code"]
    if code == "success":
        dataList = []
        ageList = []
        devList = []
        tmpDic = {}
        for item in data["result"]:
            equipCode = item["equipCode"]  # 装备编码
            equipName = item["equipName"]  # 装备名称
            equipData = item["equipData"]  # 装备数据
            for ed in equipData:
                metricName = ed["metricName"]  # 测点名称
                metricCode = ed["metricCode"]  # 测点编码
                metricData = ed["metricData"]  # 测点数据
                devKey = equipName + metricName
                for md in metricData:
                    timestamp = md["timestamp"]  # 时间戳
                    metricValue = round(float(md["metricValue"]), 4)  # 测点值
                    if devKey in tmpDic.keys():
                        tmpDic[devKey].append(metricValue)
                    else:
                        tmpDic[devKey] = [metricValue]
            ageList.append(len(equipData))
            devList.append(equipName)

        for key in tmpDic.keys():
            dataList.append(tmpDic[key])
        return dataList, ageList, devList
    else:
        return None, None, None


# ---计算SOH 数据结构
# 设备1  时间戳  测点1 测点2
# 设备1  时间戳  测点1 测点2
# 设备2  时间戳  测点1 测点2
# 设备2  时间戳  测点1 测点2

# 生成计算SOH、SOC、内阻不平衡度、电压不平衡度格式数据
def process_zb_history_data_soh(data, mapping):
    if data is None:
        return None
    code = data["code"]
    if code == "success":
        retData = []
        tmpDic = {}
        for item in data["result"]:
            equipCode = item["equipCode"]  # 装备编码
            equipName = item["equipName"]  # 装备名称
            equipData = item["equipData"]  # 装备数据
            for ed in equipData:
                metricName = ed["metricName"]  # 测点名称

                # 兼容未绑定的测点
                if metricName not in mapping.keys():
                    continue

                metricCode = ed["metricCode"]  # 测点编码
                metricData = ed["metricData"]  # 测点数据
                for i, md in enumerate(metricData):
                    devKey = equipName + "#" + str(i)
                    timestamp = md["timestamp"]  # 时间戳
                    metricValue = md["metricValue"]  # 测点值
                    mappingMetricName = mapping[metricName]
                    if devKey in tmpDic.keys():
                        tmpDic[devKey].update({mappingMetricName: metricValue})
                    else:
                        timestampLong = TimeUtils.convert_time_stamp(timestamp)
                        tmpDic[devKey] = {"ts": timestampLong, "did": equipCode, mappingMetricName: metricValue}
        for key in tmpDic.keys():
            retData.append(tmpDic[key])
        return retData
    else:
        return None


# 计算自相关的数据格式
# 设备1 时间段 测点1 测点2
# 设备2 时间段 测点1 测点2

# 生成自相关数据格式
def process_zb_history_data_relation(data, subfrom, subto):
    if data is None:
        return None, None, None, None
    code = data["code"]
    if code == "success":
        dataList = []
        subDataList = []
        devList = []
        keyList = []
        tmpDic = {}
        subTmpDic = {}
        for item in data["result"]:
            equipCode = item["equipCode"]  # 装备编码
            equipName = item["equipName"]  # 装备名称
            equipData = item["equipData"]  # 装备数据
            for ed in equipData:
                metricName = ed["metricName"]  # 测点名称
                metricCode = ed["metricCode"]  # 测点编码
                metricData = ed["metricData"]  # 测点数据
                devKey = equipName + metricName
                for md in metricData:
                    timestamp = md["timestamp"]  # 时间戳
                    metricValue = md["metricValue"]  # 测点值
                    if devKey in tmpDic.keys():
                        tmpDic[devKey].append(metricValue)
                    else:
                        tmpDic[devKey] = [metricValue]
                    if subfrom == -1 or subto == -1:
                        pass
                    else:
                        timestampLong = TimeUtils.convert_time_stamp(timestamp)
                        if subfrom <= timestampLong <= subto:
                            if devKey in subTmpDic.keys():
                                subTmpDic[devKey].append(metricValue)
                            else:
                                subTmpDic[devKey] = [metricValue]

            devList.append(equipName)

        for key in tmpDic.keys():
            dataList.append(tmpDic[key])
            keyList.append(key)
            if key in subTmpDic.keys():
                subDataList.append(subTmpDic[key])
            else:
                subDataList.append([])

        return dataList, subDataList, devList, keyList
    else:
        return None, None, None, None


# 查询测点映射
def query_metric_mapping(equipTypeCode):
    with httpx.Client(timeout=constants.REST_REQUEST_TIMEOUT, verify=False) as client:
        url = constants.URL_MD_QUERY_METRIC_MAPPING
        r = client.get(url, params={"equipTypeCode": equipTypeCode})
        dataS = r.json()
        return dataS
    return None


# 通过装备类型编码查询装备类型
def query_equip_type_by_equip_type_code(equipTypeCode):
    with httpx.Client(timeout=constants.REST_REQUEST_TIMEOUT, verify=False) as client:
        url = constants.URL_MD_QUERY_EQUIP_TYPE_BY_EQUIP_TYPE_CODE
        r = client.get(url, params={"equipTypeCode": equipTypeCode})
        return r.text
    return ""
