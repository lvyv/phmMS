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
from numpy import where
from sklearn.datasets import make_classification
from matplotlib import pyplot


def demo1():
    # 定义数据集
    X, y = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 为每个类的样本创建散点图
    for class_value in range(2):
        # 获取此类的示例的行索引
        row_ix = where(y == class_value)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo2():
    # 亲和力传播聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import AffinityPropagation
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = AffinityPropagation(damping=0.9)
    # 匹配模型
    model.fit(X)
    # 为每个示例分配一个集群
    yhat = model.predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo3():
    # 聚合聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import AgglomerativeClustering
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = AgglomerativeClustering(n_clusters=2)
    # 模型拟合与聚类预测
    yhat = model.fit_predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo4():
    # birch聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import Birch
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = Birch(threshold=0.01, n_clusters=2)
    # 适配模型
    model.fit(X)
    # 为每个示例分配一个集群
    yhat = model.predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo5():
    # dbscan 聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import DBSCAN
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = DBSCAN(eps=0.30, min_samples=9)
    # 模型拟合与聚类预测
    yhat = model.fit_predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo6():
    # k-means 聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import KMeans
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = KMeans(n_clusters=2)
    # 模型拟合
    model.fit(X)
    # 为每个示例分配一个集群
    yhat = model.predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo7():
    # 均值漂移聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import MeanShift
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = MeanShift()
    # 模型拟合与聚类预测
    yhat = model.fit_predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo8():
    # optics聚类
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import OPTICS
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = OPTICS(eps=0.8, min_samples=10)
    # 模型拟合与聚类预测
    yhat = model.fit_predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo9():
    # spectral clustering
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import SpectralClustering
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = SpectralClustering(n_clusters=2)
    # 模型拟合与聚类预测
    yhat = model.fit_predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


def demo10():
    # 高斯混合模型
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.mixture import GaussianMixture
    from matplotlib import pyplot
    # 定义数据集
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                               random_state=4)
    # 定义模型
    model = GaussianMixture(n_components=2)
    # 模型拟合
    model.fit(X)
    # 为每个示例分配一个集群
    yhat = model.predict(X)
    # 检索唯一群集
    clusters = unique(yhat)
    # 为每个群集的样本创建散点图
    for cluster in clusters:
        # 获取此群集的示例的行索引
        row_ix = where(yhat == cluster)
        # 创建这些样本的散布
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # 绘制散点图
    pyplot.show()


if __name__ == "__main__":
    demo10()
