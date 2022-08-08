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
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib import patches as mpatches
from mpl_toolkits.mplot3d import Axes3D


# 测试类 2D聚类绘制
def draw_2d(objpos, pos, df2, dfnew, agelist, datumn):
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


# 测试类 3D聚类绘制
def draw_3D(objpos, pos, df2, dfnew, agelist, datumn):
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
        draw_3D(objpos, pos, df2, dfnew, agelist, datumn)
    else:
        draw_2d(objpos, pos, df2, dfnew, agelist, datumn)
