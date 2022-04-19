import requests
import json
import time

from common import cluster, mds
import logging
from physics.common.cluster_utils import cluster_shape
from physics.test.drawModel import model_draw
from services.convert.cluster_display_util import ClusterDisplayUtil


def get_data_and_age(dataS):
    dataList = []
    ageList = []
    for key in dataS.keys():
        ks = dataS[key].keys()
        for k in ks:
            dataList.append(dataS[key][k])
        ageList.append(len(ks))
    return dataList, ageList


#    frequencies, spectrum = cluster.ts2fft(dataList, 20480, 2048)

# 2D聚类  name, size, color, shape, x, y
def calculate_cluster_2d(dataList, ageList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    pos = mds.compute_mds_pos(dataList, 2)

    df2.loc[:, 'color'] = '#000000'
    for idx, elems in enumerate(dfnew['vectors']):
        for el in elems:
            df2.loc[el, 'color'] = dfnew.loc[idx, 'color']

    # model_draw(len(dataList), pos, df2, dfnew, ageList, dataList, 2)

    df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)

    df2['shape'] = 0
    start = 0
    for i, item in enumerate(ageList):
        df2.loc[start:, 'shape'] = cluster_shape[i % len(cluster_shape)]
        start += item

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]

    return df2.to_json()


# 3D聚类 name, size, color, shape, x, y, z
def calculate_cluster_3d(dataList, ageList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    pos = mds.compute_mds_pos(dataList, 3)

    df2.loc[:, 'color'] = '#000000'
    for idx, elems in enumerate(dfnew['vectors']):
        for el in elems:
            df2.loc[el, 'color'] = dfnew.loc[idx, 'color']

    # model_draw(len(dataList), pos, df2, dfnew, ageList, dataList, 3)

    df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)

    df2['shape'] = 0
    start = 0
    for i, item in enumerate(ageList):
        df2.loc[start:, 'shape'] = cluster_shape[i % len(cluster_shape)]
        start += item

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]
    df2['pos_z'] = pos[:, 2]

    return df2.to_json()


# 时序聚类 name,  *,  color, shape, x, y
def calculate_cluster_agg2d(dataList, ageList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    pos = mds.compute_mds_pos(dataList, 2)

    df2.loc[:, 'color'] = '#000000'
    for idx, elems in enumerate(dfnew['vectors']):
        for el in elems:
            df2.loc[el, 'color'] = dfnew.loc[idx, 'color']

    # model_draw(len(dataList), pos, df2, dfnew, ageList, dataList, 2)

    df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)

    df2['shape'] = 0
    start = 0
    for i, item in enumerate(ageList):
        df2.loc[start:, 'shape'] = cluster_shape[i % len(cluster_shape)]
        start += item

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]

    return df2.to_json()


# 聚类时间演化 name, *, color, *, x, y, *
def calculate_cluster_agg3d(dataList, ageList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    pos = mds.compute_mds_pos(dataList, 2)

    df2.loc[:, 'color'] = '#000000'
    for idx, elems in enumerate(dfnew['vectors']):
        for el in elems:
            df2.loc[el, 'color'] = dfnew.loc[idx, 'color']

    # model_draw(len(dataList), pos, df2, dfnew, ageList, dataList, 2)

    df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)

    df2['shape'] = 0
    start = 0
    for i, item in enumerate(ageList):
        df2.loc[start:, 'shape'] = cluster_shape[i % len(cluster_shape)]
        start += item
    # TODO FIX x坐标取时间
    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 0]
    df2['pos_z'] = pos[:, 1]
    return df2.to_json()


def calculate_cluster(dataS, display):
    try:
        out = None
        dataList, ageList = get_data_and_age(dataS)
        if display == ClusterDisplayUtil.DISPLAY_2D:
            out = calculate_cluster_2d(dataList, ageList)
        elif display == ClusterDisplayUtil.DISPLAY_3D:
            out = calculate_cluster_3d(dataList, ageList)
        elif display == ClusterDisplayUtil.DISPLAY_AGG2D:
            out = calculate_cluster_agg2d(dataList, ageList)
        elif display == ClusterDisplayUtil.DISPLAY_AGG3D:
            out = calculate_cluster_agg3d(dataList, ageList)
        else:
            pass
    except requests.exceptions.ConnectionError as ce:
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


def calculate_relate(inData, leftTag, rightTag, step, unit):
    res = {"B001": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]},
           "B002": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]}}
    return res


def relate_convert(dataS):
    inDatas = json.loads(json.dumps(dataS))
    return inDatas


def evaluate_soh(did):
    """
    计算soh和扩展指标的值并返回。
    :param did:
    :return:
    """
    logging.info(did)
    return 0.99, {"soc": 0.8, "Rimbalance": 0.1}


# {
# 	"dev1": {
# 		"ts": [1, 2, 3, 4],
# 		"metric1": [1, 2, 3, 5],
# 		"metric2": [2, 3, 4, 5]
# 	},
# 	"dev2": {
# 		"ts": [1, 2, 3, 4],
# 		"metric1": [1, 2, 3, 4],
# 		"metric2": [2, 3, 4, 5]
# 	}
# }
def calculate_soh(dataS):
    devs = dataS.keys()
    results = {}
    for dev in devs:
        ts = int(time.time() * 1000)
        soh, extend = evaluate_soh(dev)
        results.update({dev: {'soh': soh, 'extend': extend, 'ts': ts}})
    return results


def soh_convert(dataS):
    inDatas = json.loads(json.dumps(dataS))
    return inDatas
