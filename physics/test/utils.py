import pandas as pd
import scipy.fftpack
import scipy.io


# 读取mat数据
def load_mat(file, path):
    strf = f'{path}{file}'
    data = scipy.io.loadmat(strf)
    # fid = '{:0>3}'.format(file)  # 99 --> 099
    fileid = [int(si) for si in file.split('.') if si.isdigit()][0]  # xx.97.mat now changed to 97
    width = 3
    fid = f'{fileid:0{width}d}'  # 97 -> 097, and 100 -> 100
    de = data[f'X{fid}_DE_time']
    fe = data[f'X{fid}_FE_time']
    # drive end amplitude
    ampde = []
    for i in range(de.shape[0]):
        ampde.append(de[i][0])
    # fan end amplitude
    ampfe = []
    for i in range(fe.shape[0]):
        ampfe.append(fe[i][0])

    return ampde, ampfe


# 加载csv格式数据
def load_csv(file, path, ns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8']):
    strf = f'{path}{file}'
    df = pd.read_table(strf, names=ns)
    c1 = df.iloc[:, 0].values
    c2 = df.iloc[:, 1].values
    c3 = df.iloc[:, 2].values
    c4 = df.iloc[:, 3].values
    c5 = df.iloc[:, 4].values
    c6 = df.iloc[:, 5].values
    c7 = df.iloc[:, 6].values
    c8 = df.iloc[:, 7].values
    return c1, c2, c3, c4, c5, c6, c7, c8


def load_dat(file, path, ns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8']):
    return load_csv(file, path, ns)

