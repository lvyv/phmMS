from random import random, choice

import numpy as np
import requests
import json

from phmconfig import constants
from physics.common import cluster, mds
import logging
from physics.common.cluster_utils import cluster_shape
from statsmodels.tsa.api import stattools
from services.convert.cluster_display_util import ClusterDisplayUtil
from physics.transport import dataCenter
from scipy.stats import pearsonr


def compute_df_color(df2, dfnew):
    df2.loc[:, 'color'] = '#000000'
    for idx, elems in enumerate(dfnew['vectors']):
        for el in elems:
            df2.loc[el, 'color'] = dfnew.loc[idx, 'color']


def drop_df_data(df2):
    df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)


def compute_df_shape(df2, ageList):
    df2['shape'] = 0
    start = 0
    for i, item in enumerate(ageList):
        df2.loc[start:, 'shape'] = cluster_shape[i % len(cluster_shape)]
        start += item


def compute_df_devName(df2, ageList, devList):
    start = 0
    for i, item in enumerate(ageList):
        df2.loc[start:, 'dev'] = devList[i]
        start += item


def fix_cluster_age(df):
    for idx, age in enumerate(df["age"]):
        if age >= 1000000:
            ag = 18
        elif age >= 100000:
            ag = 17 + round(age / 100000, 5)
        elif age >= 10000:
            ag = 16 + round(age / 10000, 4)
        elif age >= 1000:
            ag = 15 + round(age / 1000, 3)
        elif age >= 100:
            ag = 14 + round(age / 1000, 3)
        elif age >= 90:
            ag = 13 + round(age / 100, 2)
        elif age >= 80:
            ag = 12 + round(age / 90, 2)
        elif age >= 70:
            ag = 11 + round(age / 80, 2)
        elif age >= 60:
            ag = 10 + round(age / 70, 2)
        elif age >= 50:
            ag = 9 + round(age / 60, 2)
        elif age >= 40:
            ag = 8 + round(age / 50, 2)
        elif age >= 30:
            ag = 7 + round(age / 40, 2)
        elif age >= 20:
            ag = 6 + round(age / 30, 2)
        elif age >= 10:
            ag = 5 + round(age / 20, 2)
        elif age >= 5:
            ag = 4 + round(age / 10, 2)
        else:
            ag = 3 + round(age / 5, 2)
        df.loc[idx, 'age'] = ag


#    frequencies, spectrum = cluster.ts2fft(dataList, 20480, 2048)

# 2D聚类  name, size, color, shape, x, y
def calculate_cluster_2d(dataList, ageList, devList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    logging.info("2D HDBSCAN calculate complete")
    df2 = mds.dev_age_compute(dataList, ageList)
    fix_cluster_age(df2)
    logging.info("2D age calculate complete")
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(dataList, 2)
    logging.info("2D pos calculate complete")
    compute_df_color(df2, dfnew)
    drop_df_data(df2)
    compute_df_shape(df2, ageList)

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]

    return df2.to_json()


# 3D聚类 name, size, color, shape, x, y, z
def calculate_cluster_3d(dataList, ageList, devList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    logging.info("3D HDBSCAN calculate complete")
    df2 = mds.dev_age_compute(dataList, ageList)
    logging.info("3D age calculate complete")
    fix_cluster_age(df2)
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(dataList, 3)
    logging.info("3D pos calculate complete")
    compute_df_color(df2, dfnew)
    drop_df_data(df2)
    compute_df_shape(df2, ageList)

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]
    df2['pos_z'] = pos[:, 2]

    return df2.to_json()


# 时序聚类 name,  *,  color, shape, x, y
def calculate_cluster_agg2d(dataList, ageList, devList):
    frequencies, spectrumn = cluster.ts2fft(dataList)
    logging.info("agg2d fft calculate complete")
    _, dfnew = cluster.cluster_vectors(spectrumn, False)
    logging.info("agg2d HDBSCAN calculate complete")
    df2 = mds.dev_age_compute(spectrumn, ageList, frequencies)
    logging.info("agg2d age calculate complete")
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(spectrumn, 2)
    logging.info("agg2d pos calculate complete")
    compute_df_color(df2, dfnew)
    drop_df_data(df2)
    compute_df_shape(df2, ageList)

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]

    return df2.to_json()


# 聚类时间演化 name, *, color, *, x, y, *
def calculate_cluster_agg3d(dataList, ageList, devList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    logging.info("agg3d HDBSCAN calculate complete")
    df2 = mds.dev_age_compute(dataList, ageList)
    logging.info("agg3d age calculate complete")
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(dataList, 2)
    logging.info("agg3d pos calculate complete")
    compute_df_color(df2, dfnew)
    drop_df_data(df2)
    compute_df_shape(df2, ageList)

    # TODO FIX x坐标取时间
    df2['pos_x'] = df2['age']
    df2['pos_y'] = pos[:, 0]
    df2['pos_z'] = pos[:, 1]
    return df2.to_json()


def calculate_cluster(dataS, display):
    try:
        logging.info("start cluster =>" + display)
        out = None
        if display == ClusterDisplayUtil.DISPLAY_2D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_2d_3d_agg3d(dataS)
            logging.info("2d cluster data prepare to complete")
            out = calculate_cluster_2d(dataList, ageList, devList)
        elif display == ClusterDisplayUtil.DISPLAY_3D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_2d_3d_agg3d(dataS)
            logging.info("3d cluster data prepare to complete")
            out = calculate_cluster_3d(dataList, ageList, devList)
        elif display == ClusterDisplayUtil.DISPLAY_AGG2D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_agg2d(dataS)
            logging.info("agg2d cluster data prepare to complete")
            out = calculate_cluster_agg2d(dataList, ageList, devList)
        elif display == ClusterDisplayUtil.DISPLAY_AGG3D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_2d_3d_agg3d(dataS)
            logging.info("agg3d cluster data prepare to complete")
            out = calculate_cluster_agg3d(dataList, ageList, devList)
        else:
            pass
        logging.info("complete cluster =>" + display)
    except Exception as ce:
        logging.info("stop cluster =>" + display)
        logging.error(ce)
    return out


def cluster_convert(dataS):
    inDatas = json.loads(dataS)
    outDatas = {}
    keys = inDatas.keys()
    for key in keys:
        innerKeys = inDatas[key].keys()
        for innerKey in innerKeys:
            if innerKey in outDatas.keys():
                outDatas[innerKey].append(inDatas[key][innerKey])
            else:
                outDatas[innerKey] = [inDatas[key][innerKey]]
    return outDatas


# res = {"B001": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]},
#        "B002": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]}}
def calculate_relate(inData, subFrom, subTo):
    x, y, devList, keyList = dataCenter.process_zb_history_data_relation(inData, subFrom, subTo)
    res = {}
    for keyIndex,  key in enumerate(keyList):
        res.update({key: {"lag": [], "value": []}})
        # TODO 自相关模型 目前支持自相关模型
        if subFrom == -1 and subTo == -1 or len(y[keyIndex]) <= 1:
            acf = stattools.acf(x[keyIndex], adjusted=True)
            for index, item in enumerate(acf):
                res[keyList[keyIndex]]["lag"].append(index)
                res[keyList[keyIndex]]["value"].append(item)
        else:
            x_len = len(x[keyIndex])
            y_len = len(y[keyIndex])
            if constants.METHOD_ZLX_TYPE == 1:
                for start in range(0, x_len, y_len):
                    if start + y_len > x_len:
                        break
                    ccf = stattools.ccf(x[keyIndex][start: start + y_len], y[keyIndex])
                    for index, item in enumerate(ccf):
                        res[keyList[keyIndex]]["lag"].append(start + index)
                        res[keyList[keyIndex]]["value"].append(item)
            else:
                i = 0
                for start in range(0, x_len, min(1, y_len)):
                    if start + y_len > x_len:
                        break
                    k, _ = pearsonr(x[keyIndex][start: start + y_len], y[keyIndex])
                    res[keyList[keyIndex]]["lag"].append(i)
                    _value = 0 if np.isnan(k) else round(k, 5)
                    res[keyList[keyIndex]]["value"].append(_value)
                    i = i + 1
    return res


#  TODO  fix 评估模型计算
def evaluate_soh(datas, devType):

    # 根据devType 计算不同测测量指标
    logging.info("参数评估模型计算的设备类型为:" + devType)

    # in
    # [{'ts':时间戳, 'did': 'BATTERY', '测点1':'值1', '测点2':'值2' }]
    # 进行 健康指标（FM1） 内阻不平衡度(FM2) 电压不平衡度(FM3) 健康状态(IM1)
    for item in datas:
        item.update({"FM1": int(random() * 100),
                     "FM2": int(random() * 100),
                     "FM3": int(random() * 100),
                     "IM1": choice([0, 1, 2])})
    return datas


# [{
# "equipCode": "B001",
# "equipName": "电池A",
# "equipData": [{
#     "metricName": "容量",
#     "metricCode": "M001",
#     "metricData": [{
#         "timestamp": "2022-05-18 00:00:00",
#         "metricValue": 0.5
#     }]
#   }]
# }]

def calculate_soh(dataS, mappingS, dev_type):
    #  返回设备数据
    devDatas = dataCenter.process_zb_history_data_soh(dataS, mappingS)
    try:
        # 进行 SOH、SOC、 内阻不平衡度、健康状态
        evaluate_soh(devDatas, dev_type)
    finally:
        pass
    # 返回数据
    return devDatas
