import requests
import json

from common import cluster, mds
import logging
from physics.common.cluster_utils import cluster_shape
from physics.test.drawModel import model_draw


# 数据通过模型清洗
def model_invoke(dataS, dimension):
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


def model_convert(inDatas):
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


