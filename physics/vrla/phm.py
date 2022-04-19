import requests
import json
import time

from common import cluster, mds
import logging
from physics.common.cluster_utils import cluster_shape
from physics.test.drawModel import model_draw


def calculate_cluster(dataS, dimension):
    try:
        datumn = []
        agelist = []
        for key in dataS.keys():
            ks = dataS[key].keys()
            for k in ks:
                datumn.append(dataS[key][k])
            agelist.append(len(ks))

        objpos = len(datumn)
        frequencies, spectrum = cluster.ts2fft(datumn, 20480, 2048)
        clusternew_, dfnew = cluster.cluster_vectors(spectrum, False)
        df2 = mds.dev_age_compute(spectrum, frequencies, agelist)
        pos = mds.compute_mds_pos(spectrum, dimension)
        df2.loc[:, 'color'] = '#000000'
        for idx, elems in enumerate(dfnew['vectors']):
            for el in elems:
                df2.loc[el, 'color'] = dfnew.loc[idx, 'color']
        logging.info(f'1.MDS pos computed.')
        model_draw(objpos, pos, df2, dfnew, agelist, datumn, dimension)
        logging.info('2.MDS plot finished.')
        df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)
        df2['shape'] = 0
        start = 0
        for i, item in enumerate(agelist):
            df2.loc[start:, 'shape'] = cluster_shape[i % len(cluster_shape)]
            start += item
        df2['pos_x'] = pos[:, 0]
        df2['pos_y'] = pos[:, 1]
        if dimension == 3:
            df2['pos_z'] = pos[:, 2]
        json.loads(df2.to_json())
        logging.info('3.Return to main procedure.')
        out = df2.to_json()
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
