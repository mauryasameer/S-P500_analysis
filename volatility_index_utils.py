import numpy as np
import pandas as pd

def bollinger_mavg(close, n=7):
    mavg = close.rolling(n, min_periods=0).mean()
    return pd.Series(mavg, name='mavg')


def bollinger_hband(close, n=7, ndev=2):
    mavg = close.rolling(n, min_periods=0).mean()
    mstd = close.rolling(n, min_periods=0).std()
    hband = mavg + ndev*mstd
    return pd.Series(hband, name='hband')


def bollinger_lband(close, n=7, ndev=2):
    mavg = close.rolling(n, min_periods=0).mean()
    mstd = close.rolling(n, min_periods=0).std()
    lband = mavg - ndev * mstd
    return pd.Series(lband, name='lband')

def average_true_range(high, low, close, n=7):
    cs = close.shift(1)
    tr = high.combine(cs, max) - low.combine(cs, min)

    atr = np.zeros(len(close))
    atr[0] = tr[1::].mean()
    for i in range(1, len(atr)):
        atr[i] = (atr[i-1] * (n-1) + tr.iloc[i]) / float(n)

    atr = pd.Series(data=atr, index=tr.index)

    return pd.Series(atr, name='atr')

def donchian_channel_hband(close, n=7, fillna=False):
    hband = close.rolling(n, min_periods=0).max()
    if fillna:
        hband = hband.replace(
            [np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(hband, name='dchband')


def donchian_channel_lband(close, n=7, fillna=False):
    lband = close.rolling(n, min_periods=0).min()
    if fillna:
        lband = lband.replace(
            [np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(lband, name='dclband')