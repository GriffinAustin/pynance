"""
Functions for generating features.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

These functions are intended to be used in conjunction
with `functools.partial` to pass to `data.labeledfeatures()`.
For example,

>>> from functools import partial
>>> features, labels = pn.data.labeledfeatures(eqdata, 
        partial(pn.data.feat.growth_vol(256, 252, 'Adj Close'), labelfunc)
"""

from functools import partial

import numpy as np
import pandas as pd

def growth_vol(n_sessions, eqdata, **kwargs):
    """
    Combine growth and volume data into a set of features.

    Parameters
    --
    n_sessions : int
        Number of sessions over which price and volume will be
        used as features.

    eqdata : DataFrame
        Data from which to build features.

    averaging_interval : int, optional
        Interval over which to average volume. Defaults to 252 (1 year).

    pricecol : str, optional
        Column to use for prices. Defaults to 'Adj Close'

    skipatend : int, optional
        Rows to skip at the end. Used for synchronizing the indices of
        labels and features. Defaults to 0.

    constfeat : bool, optional
        Determines whether or not the constant 1. will appear
        as first feature in each row. Defaults to `True`.

    Returns
    --
    features : DataFrame
        The feature set determined by the input parameters.

    skipatstart : int
        The row number of the first feature
        as measured within the index of `eqdata`. This is 
        used when the function is passed to `labeledfeatures()`
        for synchronizing labels with features.
    """
    _averaging_interval = kwargs.get('averaging_interval', 252)
    _pricecol = kwargs.get('pricecol', 'Adj Close')
    _skipatend = kwargs.get('skipatend', 0)
    _skipatstart = n_sessions + _averaging_interval - 1
    _growth = growth(eqdata, selection=_pricecol, skipstartrows=(_averaging_interval - 1),
        skipendrows=_skipatend)
    _vol = ratio_to_ave(eqdata, _averaging_interval, skipendrows=_skipatend)
    _features = _featurize_growth_vol(_growth, _vol, n_sessions) 
    if kwargs.get('constfeat', True):
        _features = add_const(_features)
    return _features, _skipatstart

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
    tmpdata = featurize(eqdata, averaging_interval, selection=selection)
    averages = tmpdata.mean(axis=1)
    avesize = len(averages.index)
    resultdata = eqdata.loc[:, selection].values[(skipstartrows + averaging_interval):(datasize - skipendrows)] / \
            averages.values[skipstartrows:(avesize - skipendrows - 1)]
    resultindex = eqdata.index[(skipstartrows + averaging_interval):(datasize - skipendrows)]
    return pd.DataFrame(data=resultdata, index=resultindex, columns=[outputcol], dtype='float64')

def featurize(equity_data, n_sessions, **kwargs):
    """
    featurize(equity_data, n_sessions, **kwargs)

    Generate a raw (unnormalized) feature set from the input data.
    The value at `column` on the given date is taken
    as a feature, and each row contains values for n_sessions

    Parameters
    ---
    equity_data : DataFrame
        data from which to generate features

    n_sessions : int
        number of sessions to use as features

    selection : str, default: 'Adj Close'
        column of `equity_data` from which to generate features.

    columns : list, default: map(str, range((-n_sessions + 1), 1))
        column names for output DataFrame. Default will look like:
        ['-5', '-4', '-3', '-2', '-1', '0']

    Returns
    --
    out : DataFrame
        Each row is a sequence of `n_sessions` session values where
        the last column matches the value on the date specified by
        the DataFrame index.

    Benchmarking
    ---
    >>> s = 'from __main__ import data\nimport datetime as dt\n'
    >>> timeit.timeit('data.featurize(data.get("ge", dt.date(1960, 1, 1), 
            dt.date(2014, 12, 31)), 256)', setup=s, number=1)
    1.6771750450134277
    """
    columns = kwargs.get('columns', map(str, range(-n_sessions + 1, 1)))
    selection = kwargs.get('selection', 'Adj Close')
    # empty DataFrame with desired index and column labels
    features = pd.DataFrame(index=equity_data.index[(n_sessions - 1):],
            columns=columns, dtype='float64')
    values = equity_data[selection].values
    for i in range(n_sessions - 1):
        features.iloc[:, i] = values[i:(-n_sessions + i + 1)]
    features.iloc[:, n_sessions - 1] = values[(n_sessions - 1):]
    return features

def add_const(features):
    """
    Prepend the constant feature 1 as first feature and return the modified
    feature set.

    Parameters
    --
    features : ndarray or DataFrame
    """
    content = np.empty((features.shape[0], features.shape[1] + 1), dtype='float64')
    content[:, 0] = 1.
    if isinstance(features, np.ndarray):
        content[:, 1:] = features
        return content
    content[:, 1:] = features.iloc[:, :].values
    cols = ['Constant'] + features.columns.tolist()
    return pd.DataFrame(data=content, index=features.index, columns=cols, dtype='float64')

def _featurize_growth_vol(growth, volume, n_sessions):
    """
    Combine growth and volume data into a set of features
    """
    growth_feat = featurize(growth, n_sessions, selection='Growth')
    vol_feat = featurize(volume, n_sessions, selection='Rel Vol')
    growth_cols = map(partial(_concat, strval='G'), range(-n_sessions + 1, 1))
    vol_cols = map(partial(_concat, strval='V'), range(-n_sessions + 1, 1))
    all_cols = list(growth_cols) + list(vol_cols)
    features = pd.DataFrame(index=growth_feat.index, columns=all_cols, dtype='float64')
    features.iloc[:, :n_sessions] = growth_feat.values
    features.iloc[:, n_sessions:] = vol_feat.values
    return features

def _concat(intval, strval):
    """ helper for creating columns in `_featurize_growth_vol()` """
    return str(intval) + strval
