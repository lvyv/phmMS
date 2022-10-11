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
import math
import time
import pandas as pd
from pathlib import Path

mappings = {"Voltage_measured": "测量的电压",
            "Current_measured": "测量的电流",
            "Temperature_measured": "工作温度",
            "Current_charge": "充电电流",
            "Voltage_charge": "充电电压",
            "Capacity": "容量2",
            "Datatime": "时间",
            "Operation_type": "类型",
            "Ambient_temperature": "环境温度",
            "SOH": "健康指标",
            "SOC": "容量",
            "Cycle": "充电次数",
            "internal_resistance": "内阻"}

BList = ["B001", "B002", "B003", "B004", "B005", "B006", "B007", "B008", "B009", "B010",
         "B011", "B012", "B013", "B014", "B015", "B016", "B017", "B018", "B019", "B020",
         "B021", "B022", "B023", "B024", "B025", "B026", "B027", "B028", "B029", "B030",
         "B031", "B032", "B033", "B034", "B035", "B036", "B037", "B038", "B039", "B040"]
nasaDataPath = Path(Path(__file__).parent).joinpath("nasaData")
nameSpace = mappings.keys()


# 加载csv格式数据
def load_csv(path, file, ns):

    tmpPathPrefix = path.joinpath(file)
    strf = f'{tmpPathPrefix}.csv'
    df = pd.read_csv(strf, names=ns)
    # size = len(ns)
    # for index in range(size):
    #     c = df.iloc[:, index].values
    # dfs = df["SOC"].tolist()
    # dfs.remove("SOC")
    return df


def makeTime(startTime, endTime, data_len, index):
    start = TimeUtil.convert_time_stamp(startTime)
    end = TimeUtil.convert_time_stamp(endTime)
    # int(down)  ceil(up) round(四舍五入)
    interval = round((end - start) / 1000 / data_len)
    # interval = 5
    return TimeUtil.convert_time_str(start + index * interval * 1000)


def convert(equipCode, metricName, startTime, endTime, maxPoints=200):
    # 设备分割
    deviceIds = equipCode.split(",")
    metricIds = metricName.split(",")

    # 生成模拟数据
    ret = {
        "code": "success",
        "result": []
    }
    tagNumber = 1
    for dev in BList:
        if dev not in deviceIds:
            continue
        # 加载数据
        loadData = load_csv(nasaDataPath, dev, nameSpace)
        genDev = {
            "equipCode": dev,
            "equipName": dev,
            "equipData": []
        }
        for key in mappings.keys():
            if mappings.get(key) not in metricIds:
                continue
            genTag = {
                "metricName": mappings[key],
                "metricCode": "M00" + str(tagNumber),
                "metricData": []
            }
            data = loadData[key].tolist()
            data.remove(key)
            data_len = len(data)
            for index, itval in enumerate(data):
                if index < maxPoints:
                    genTag["metricData"].append({
                        "timestamp": makeTime(startTime, endTime, data_len, index),
                        "metricValue":  0 if math.isnan(float(itval)) else itval
                    })
            genDev["equipData"].append(genTag)
            tagNumber = tagNumber + 1
        ret["result"].append(genDev)
    return ret


class TimeUtil:

    @staticmethod
    def convert_time_stamp(timeStr):
        # 2022-02-13 22:09:59
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp * 1000

    @staticmethod
    def convert_time_str(timestamp):
        time_tuple = time.localtime(timestamp / 1000)
        bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        # print("北京时间:", bj_time)
        return bj_time


if __name__ == "__main__":
    load_csv(nasaDataPath, "B001", nameSpace)
    convert("B001,B002", "容量,健康指标", "2022-10-09 10:00:00", "2022-10-09 12:00:00")
