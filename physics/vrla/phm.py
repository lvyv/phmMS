import requests
import json
import time

from physics.common import cluster, mds
import logging
from physics.common.cluster_utils import cluster_shape
from statsmodels.tsa.api import stattools
from services.convert.cluster_display_util import ClusterDisplayUtil
from physics.transport import dataCenter


def get_data_and_age(dataS):
    dataList = []
    ageList = []
    for key in dataS.keys():
        ks = dataS[key].keys()
        for k in ks:
            dataList.append(dataS[key][k])
        ageList.append(len(ks))
    return dataList, ageList


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
    start = 0;
    for i, item in enumerate(ageList):
        df2.loc[start:, 'dev'] = devList[i]
        start += item


#    frequencies, spectrum = cluster.ts2fft(dataList, 20480, 2048)

# 2D聚类  name, size, color, shape, x, y
def calculate_cluster_2d(dataList, ageList, devList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(dataList, 2)
    compute_df_color(df2, dfnew)
    drop_df_data(df2)
    compute_df_shape(df2, ageList)

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]

    return df2.to_json()


# 3D聚类 name, size, color, shape, x, y, z
def calculate_cluster_3d(dataList, ageList, devList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(dataList, 3)
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
    _, dfnew = cluster.cluster_vectors(spectrumn, False)
    df2 = mds.dev_age_compute(spectrumn, ageList, frequencies)
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(spectrumn, 2)

    compute_df_color(df2, dfnew)
    drop_df_data(df2)
    compute_df_shape(df2, ageList)

    df2['pos_x'] = pos[:, 0]
    df2['pos_y'] = pos[:, 1]

    return df2.to_json()


# 聚类时间演化 name, *, color, *, x, y, *
def calculate_cluster_agg3d(dataList, ageList, devList):
    _, dfnew = cluster.cluster_vectors(dataList, False)
    df2 = mds.dev_age_compute(dataList, ageList)
    compute_df_devName(df2, ageList, devList)
    pos = mds.compute_mds_pos(dataList, 2)

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
        out = None
        if display == ClusterDisplayUtil.DISPLAY_2D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_2d_3d_agg3d(dataS)
            out = calculate_cluster_2d(dataList, ageList, devList)
        elif display == ClusterDisplayUtil.DISPLAY_3D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_2d_3d_agg3d(dataS)
            out = calculate_cluster_3d(dataList, ageList, devList)
        elif display == ClusterDisplayUtil.DISPLAY_AGG2D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_agg2d(dataS)
            out = calculate_cluster_agg2d(dataList, ageList, devList)
        elif display == ClusterDisplayUtil.DISPLAY_AGG3D:
            dataList, ageList, devList = dataCenter.process_zb_history_data_2d_3d_agg3d(dataS)
            out = calculate_cluster_agg3d(dataList, ageList, devList)
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
    x, _ = get_data_and_age(inData)
    acf = stattools.acf(x[0], adjusted=True)
    res = {"B001": {"lag": [], "value": []}}
    for index, item in enumerate(acf):
        res["B001"]["lag"].append(index)
        res["B001"]["value"].append(item)
    #
    # res = {"B001": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]},
    #        "B002": {"lag": [1, 5, 10, 15, 20, 25], "value": [1.5, 2.5, 3.5, 4.5, 5.5, 1.5]}}
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
def calculate_soh(dataS, didS):
    devs = dataS.keys()
    results = {}
    for dev in didS:
        ts = int(time.time() * 1000)
        soh, extend = evaluate_soh(dev)
        results.update({dev: {'soh': soh, 'extend': extend, 'ts': ts}})
    return results


def soh_convert(dataS):
    inDatas = json.loads(json.dumps(dataS))
    return inDatas
