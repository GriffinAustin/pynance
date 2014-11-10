"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Calculate technical indicators
"""

import pandas as pd

def sma(eq_data, window=20):
    """ 
    simple moving average 

    Parameters
    ---
    eq_data : DataFrame
        must have exactly one column on which to calculate SMA
    window : int
        lookback period for sma
    """
    if len(eq_data.shape) > 1 and eq_data.shape[1] != 1:
        raise ValueError("input data must have exactly 1 column")
    ret = pd.DataFrame(index=eq_data.index, columns=['SMA'], dtype='float')
    ret.loc[:, 'SMA'] = pd.rolling_mean(eq_data, window=window).values.flatten()
    return ret

def bollinger(eq_data, window=20, k=2.0):
    """ 
    Bollinger bands

    Returns bolldf, smadf where bolldf is a DataFrame containing
    Bollinger bands with columns 'Upper' and 'Lower' and smadf contains
    the simple moving average.

    Parameters
    ---
    eq_data : DataFrame
        must have exactly one column on which to calculate SMA
    window : int
        lookback period for bands
    k : float
        multiple of standard deviation above and below sma
    """
    smadf = sma(eq_data, window)
    sigmas = pd.rolling_std(eq_data, window=window).values.flatten()
    bolldf = pd.DataFrame(index=eq_data.index, columns=['Upper', 'Lower'], dtype='float')
    bolldf.loc[:, 'Upper'] = smadf.iloc[:, 0].values + k * sigmas 
    bolldf.loc[:, 'Lower'] = smadf.iloc[:, 0].values - k * sigmas 
    return bolldf, smadf
