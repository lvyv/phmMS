import requests
import json
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib import patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

from common import cluster, mds
import logging
from physics.common.cluster_utils import cluster_shape


# 数据通过模型清洗
def model_invoke(dataS, dimension):
    sr = 20480  # sample rate
    ws = 2048  # window size
    try:

        datumn = []
        keys = dataS.keys()
        agelist = []
        for key in keys:
            ks = dataS[key].keys()
            for k in ks:
                datumn.append(dataS[key][k])
            agelist.append(len(ks))

        objpos = len(datumn)  # This position should be used to plot object sample.
        frequencies, spectrum = cluster.ts2fft(datumn, sr, ws)
        clusternew_, dfnew = cluster.cluster_vectors(spectrum, False)
        df2 = mds.dev_age_compute(spectrum, frequencies, agelist)  # should label at data reading phase.seg
        pos = mds.compute_mds_pos(spectrum, dimension)
        # set color for each points in df2
        df2.loc[:, 'color'] = '#000000'
        for idx, elems in enumerate(dfnew['vectors']):
            for el in elems:
                df2.loc[el, 'color'] = dfnew.loc[idx, 'color']
        logging.info(f'1.MDS pos computed.')
        model_draw(objpos, pos, df2, dfnew, agelist, datumn, dimension)
        logging.info('2.MDS plot finished.')
        df2.drop(df2.columns[list(range(len(df2.T) - 3))], axis=1, inplace=True)
        df2['shape'] = 0
        # df2.loc[objpos:, 'shape'] = 1

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
        out = df2.to_json()  # return a valid json string
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


def __draw_2d(objpos, pos, df2, dfnew, agelist, datumn):
    # plot mds scatter chart
    plt.figure(1)
    plt.axes([0., 0., 1., 1.])
    dispindices = list(range(objpos))  # only plot benchmark points.
    plt.scatter(x=pos[dispindices, 0],
                y=pos[dispindices, 1],
                s=df2.loc[dispindices, 'age'],
                label=df2.loc[dispindices, 'color'],
                edgecolors=df2.loc[dispindices, 'color'],
                facecolors='none', marker='.', alpha=0.5, lw=1)
    hnds = []
    for idx, el in enumerate(dfnew['color']):
        pop = mpatches.Patch(color=el, label=f'C: [{dfnew["cid"][idx]}], cnts:[{len(dfnew["vectors"][idx])}]')
        hnds.append(pop)
    plt.legend(handles=hnds, prop={'size': 6})
    blcnts = 2
    baselineclass = [0]
    for idx, el in enumerate(agelist[0: blcnts]):
        ps = baselineclass[idx] + el
        baselineclass.append(ps)
    # find baselineclass leader points in dfnew and
    texts = []
    for obj in baselineclass:  # 0, 24, 36, 60
        for idx, vecs in enumerate(dfnew['vectors']):
            if obj in vecs:
                txt = f'{obj} in C: [{dfnew["cid"][idx]}]'
                texts.append(plt.text(pos[obj, 0], pos[obj, 1], txt))
    adjust_text(texts)
    # label object points
    plt.scatter(x=pos[objpos:, 0],
                y=pos[objpos:, 1],
                label=df2.loc[objpos:, 'color'],
                marker='*', s=300, color='k', alpha=0.5, lw=1)
    for txt in list(range(objpos, len(datumn))):
        plt.text(pos[txt, 0], pos[txt, 1], f'PT: {txt}', c='#000000')
    plt.show()


def __draw_3D(objpos, pos, df2, dfnew, agelist, datumn):
    # plot mds scatter chart
    fig = plt.figure()
    ax = Axes3D(fig)
    dispindices = list(range(objpos))  # only plot benchmark points.
    ax.scatter(xs=pos[dispindices, 0],
               ys=pos[dispindices, 1],
               zs=pos[dispindices, 2],
               s=df2.loc[dispindices, 'age'],
               label=df2.loc[dispindices, 'color'],
               edgecolors=df2.loc[dispindices, 'color'],
               facecolors='none', marker='.', alpha=0.5, lw=1)
    hnds = []
    for idx, el in enumerate(dfnew['color']):
        pop = mpatches.Patch(color=el, label=f'C: [{dfnew["cid"][idx]}], cnts:[{len(dfnew["vectors"][idx])}]')
        hnds.append(pop)
    ax.legend(handles=hnds, prop={'size': 6})
    plt.show()


def model_draw(objpos, pos, df2, dfnew, agelist, datumn, dimension):
    if dimension == 3:
        __draw_3D(objpos, pos, df2, dfnew, agelist, datumn)
    else:
        __draw_2d(objpos, pos, df2, dfnew, agelist, datumn)
