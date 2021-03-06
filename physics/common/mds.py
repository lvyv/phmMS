import pandas as pd
import numpy as np
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA


def dev_age_compute(vectors, segment, freq=None):
    """
    This function label all the frequence domain vectors.
    ----------
    vectors : array of frequency vectors
        Each vector in vectors is nd.array type in frequency domain.
        One device's vectors begin at good health condition and run to failue,
        and then followed by another device's vectors.
    freqs : array of frequency components of a vector
        This is often used as x axis values.
    segment: list
        The segment is a list that indicates which device the vectors belong to.
    Returns
    -------
    out: DataFrame object
        Dataframe's columns are frequency components, dev, and age.
    """
    if freq is None:
        df = pd.DataFrame(vectors)
    else:
        df = pd.DataFrame(vectors, columns=freq)

    devs = []
    for iii, devnums in enumerate(segment):
        devs = devs + [iii for idx in range(devnums)]
    df['dev'] = devs

    age_factor = 1
    ptsize = []
    for iii, devnums in enumerate(segment):
        ptsize = ptsize + list(range(devnums))
    ptsize = [(pt + 1) * age_factor for pt in ptsize]
    df['age'] = ptsize
    return df


def compute_mds_pos(vectors, dimension):
    similarities = euclidean_distances(vectors)
    # vecs = np.array([list(vec) for vec in vectors])
    mds = manifold.MDS(n_components=dimension, max_iter=300, eps=1e-3,
                       dissimilarity="precomputed", n_jobs=1)
    pos = mds.fit(similarities).embedding_

    # Rescale the data
    # pos *= np.sqrt((vecs ** 2).sum()) / np.sqrt((pos ** 2).sum())

    # Rotate the data
    clf = PCA(n_components=dimension)
    # vecs = clf.fit_transform(vecs)

    pos = clf.fit_transform(pos)
    return pos
