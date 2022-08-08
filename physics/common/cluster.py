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
import numpy as np
import pandas as pd
import hdbscan
from scipy import signal
from physics.common.cluster_utils import cluster_color


def ts2fft(datumn, samplerate=1.0, nperseg=None):
    """
    This function computes all the one-dimensional time domain signals by FFT.
    Parameters
    ----------
    datumn : array of timeseries(list)
        Input signal is list array, list element contain many sample points
        in time domain.
    samplerate : int
        The sample rate of the input signals. All signals are assumed as the
        same sample rate.
    nperseg : int
        Axis over which to compute the FFT.  If not given, the last axis is
        used.
    Returns
    -------
    A tuple, `(frequencies, spectrumn_vectors)`
        The result of datumn transform by fft.
    Raises
    ------
    See Also
    --------
    Notes
    -----
    References
    ----------
    Examples
    --------
    >>>
    """
    try:
        fre = None
        spectrum_list = []
        # Because frequency domain is symmetrical, take only positive frequencies
        for idx, sig in enumerate(datumn):
            fre, amp = signal.welch(sig, fs=samplerate, scaling='density', nperseg=nperseg)
            spectrum_list.append(np.abs(amp))
    except BaseException as err:
        logging.error(err)
        fre = None
        spectrum_list = []
    return fre, spectrum_list


def cluster_vectors(vectors, predict=True):
    """
    This function cluster all the frequence domain vectors.
    ----------
    vectors : array of frequency vectors
        Each vector in vectors is nd.array type in frequency domain.
    predict : bool, optional
        Determine cluster model could be used for prediction or not.
    Returns
    -------
    A tuple, `(clustermodel, dataframe)`
        Dataframe's columns are cluster id, color, vector indices.
    Raises
    ------
    See Also
    --------
    Notes
    -----
    References
    ----------
    Examples
    --------
    >>>
    """
    cm = np.array(cluster_color)
    dat = np.array([list(vec) for vec in vectors])
    clusterer = hdbscan.HDBSCAN(min_cluster_size=10, prediction_data=predict).fit(dat)
    cids = np.unique(clusterer.labels_)
    labels = clusterer.labels_
    df = pd.DataFrame(cids, columns=['cid'])
    df['color'] = [cm[index % 32] for index in range(len(cids))]
    df['vectors'] = [list(np.where(labels == sid)[0]) for sid in cids]
    return clusterer, df
