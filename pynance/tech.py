"""
Technical analysis

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

Any function returning dataframes with only
a few columns calculated from prior data should
be located in this module.
"""

from __future__ import absolute_import

import pandas as pd

from . import common

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
        Must have exactly one column on which to calculate SMA.

    window : int, optional
        Lookback period.

    k : float
        Multiple of standard deviation above and below sma to use
        in calculating band value.

    Returns
    --
    bolldf : DataFrame
        Dataframe containing columns 'Upper' and 'Lower' describing
        the given multiple of standard deviations above and below
        simple moving average for the lookback period.

    smadf : DataFrame
        Simple moving average given the specified lookback.
    """
    smadf = sma(eq_data, window)
    sigmas = pd.rolling_std(eq_data, window=window).values.flatten()
    bolldf = pd.DataFrame(index=eq_data.index, columns=['Upper', 'Lower'], dtype='float')
    bolldf.loc[:, 'Upper'] = smadf.iloc[:, 0].values + k * sigmas 
    bolldf.loc[:, 'Lower'] = smadf.iloc[:, 0].values - k * sigmas 
    return bolldf, smadf

def growth(eqdata, **kwargs):
    """
    Generate a DataFrame where the sole column, 'Growth',
    is the growth for the equity over the given number of sessions.
    
    For example, if 'XYZ' has 'Adj Close' of `100.0` on 2014-12-15 and 
    `90.0` 4 *sessions* later on 2014-12-19, then the 'Growth' value
    for 2014-12-19 will be `0.9`.

    Parameters
    --
    eqdata : DataFrame
        Data such as that returned by `get()`

    selection : str, optional
        Column from which to determine growth values. Defaults to
        'Adj Close'.

    n_sessions : int
        Number of sessions to count back for calculating today's
        growth. For example, if `n_sessions` is set to 4, growth is
        calculated relative to the price 4 sessions ago. Defaults
        to 1 (price of previous session).

    skipstartrows : int
        Rows to skip at beginning of `eqdata` in addition to the 1 row that must
        be skipped because the calculation relies on a prior data point.
        Defaults to 0.

    skipendrows : int
        Rows to skip at end of `eqdata`. Defaults to 0.

    Returns
    --
    out : DataFrame

    Notes
    --
    The interval is the number of *sessions* between the 2 values
    whose ratio is being measured, *not* the number of days (which
    includes days on which the market is closed).

    Growth is measured relative to the earlier
    date, but the index date is the later date. This index is chosen because
    it is the date on which the value is known.
    """
    selection = kwargs.get('selection', 'Adj Close')
    n_sessions = kwargs.get('n_sessions', 1)
    skipstartrows = kwargs.get('skipstartrows', 0)
    skipendrows = kwargs.get('skipendrows', 0)
    size = len(eqdata.index)
    growthdata = eqdata.loc[:, selection].values[(skipstartrows + n_sessions):(size - skipendrows)] / \
            eqdata.loc[:, selection].values[skipstartrows:(-n_sessions - skipendrows)]
    growthindex = eqdata.index[(skipstartrows + n_sessions):(size - skipendrows)]
    return pd.DataFrame(data=growthdata, index=growthindex, columns=['Growth'], dtype='float64')

def ret(eqdata, **kwargs):
    """
    Generate a DataFrame where the sole column, 'Return',
    is the return for the equity over the given number of sessions.
    
    For example, if 'XYZ' has 'Adj Close' of `100.0` on 2014-12-15 and 
    `90.0` 4 *sessions* later on 2014-12-19, then the 'Return' value
    for 2014-12-19 will be `-0.1`.

    Parameters
    --
    eqdata : DataFrame
        Data such as that returned by `get()`

    selection : str, optional
        Column from which to determine growth values. Defaults to
        'Adj Close'.

    n_sessions : int
        Number of sessions to count back for calculating today's
        return. For example, if `n_sessions` is set to 4, return is
        calculated relative to the price 4 sessions ago. Defaults
        to 1 (price of previous session).

    skipstartrows : int
        Rows to skip at beginning of `eqdata` in addition to the 1 row that must
        be skipped because the calculation relies on a prior data point.
        Defaults to 0.

    skipendrows : int
        Rows to skip at end of `eqdata`. Defaults to 0.

    Returns
    --
    out : DataFrame

    Notes
    --
    The interval is the number of *sessions* between the 2 values
    whose ratio is being measured, *not* the number of days (which
    includes days on which the market is closed).

    The percentage gain or loss is measured relative to the earlier
    date, but the index date is the later date. The index is chose because
    that is the date on which the value is known. The percentage measure is because
    that is the way for calculating percent profit and loss.
    """
    result = growth(eqdata, **kwargs)
    result.values[:, :] -= 1.
    return result

def ratio_to_ave(eqdata, averaging_interval, **kwargs):
    """
    Return values expressed as ratios to the average over some number
    of prior sessions

    Parameters
    --
    eqdata : DataFrame

    averaging_interval : int
        Interval over which to calculate the average. Normally 252 (1 year)

    selection : str, optional
        Column to select for calculating ratio. Defaults to 'Volume'

    skipstartrows : int, optional
        Rows to skip at beginning in addition to the `averaging_interval` rows
        that must be skipped to get the baseline volume. Defaults to 0.

    skipendrows : int, optional
        Rows to skip at end. Defaults to 0.

    outputcol : str, optional
        Name of column in output dataframe.

    Returns
    --
    out : DataFrame
    """
    datasize = len(eqdata.index)
    selection = kwargs.get('selection', 'Volume')
    skipstartrows = kwargs.get('skipstartrows', 0)
    skipendrows = kwargs.get('skipendrows', 0)
    outputcol = kwargs.get('outputcol', 'Rel Vol')
    tmpdata = common.featurize(eqdata, averaging_interval, selection=selection)
    averages = tmpdata.mean(axis=1)
    avesize = len(averages.index)
    resultdata = eqdata.loc[:, selection].values[(skipstartrows + averaging_interval):(datasize - skipendrows)] / \
            averages.values[skipstartrows:(avesize - skipendrows - 1)]
    resultindex = eqdata.index[(skipstartrows + averaging_interval):(datasize - skipendrows)]
    return pd.DataFrame(data=resultdata, index=resultindex, columns=[outputcol], dtype='float64')
