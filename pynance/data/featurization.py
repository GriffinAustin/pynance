"""
Functions for generating feature sets from equity data.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

from functools import partial

import numpy as np
import pandas as pd

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

def get_growth(eqdata, **kwargs):
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

def get_return(eqdata, **kwargs):
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
    result = get_growth(eqdata, **kwargs)
    result.values[:, :] -= 1.
    return result

def labeledfeatures(eqdata, n_sessions, labelfunc, **kwargs):
    """
    Return features and labels for the given equity data.

    Each row of the features returned contains `2 * n_sessions + 1` columns
    (or 1 less if the constant feature is excluded). After the constant feature,
    if present, there will be `n_sessions` columns derived from daily growth
    of the given price column, which defaults to 'Adj Close'. There will then
    follow another `n_sessions` columns representing current volume as
    a multiple of average volume over the previous 252 (or other value determined
    by the user) sessions. 
    
    The returned features are not centered or normalized because these
    adjustments need to be made after test or cross-validation data has
    been removed.

    The constant feature is prepended by default.

    The labels are derived from `eqdata` using `labelfunc`.

    Parameters
    --
    eqdata : DataFrame
        Expected is a dataframe as return by the `get()` function. A column
        labeled 'Volume' must be present.

    n_sessions : int
        number of sessions to use as features. This is the number
        of growth and relative volume datapoints to be used in each
        row of features

    labelfunc : function
        function for deriving labels from `eqdata`. `labelfunc` must
        take 2 arguments: `df` and `pricecol`. The first
        argument is a dataframe (`labelfunc` will be applied to a slice
        of `eqdata`). The 2nd argument is the label
        used for the desired price column (Typically 'Adj Close' or 'Close').
        `labelfunc` should return a dataframe of labels followed by an int
        specifying the number of feature rows to skip at the end of the feature
        dataframe. For example, if features are relative prices 64 days out,
        these features will only be known up until 64 days before the data
        runs out. In order to properly align features and labels, the features
        should not include the last 64 rows that would otherwise be possible.

        Usage:
        `labels, skipatend = labelfunc(eqdata, pricecol)`

    pricecol : str, optional
        Column to use for price. Defaults to 'Adj Close'

    averaging_interval : int, optional
        Interval to use for generating the average volume, relative
        to which current volume will be expressed. Defaults to 252
        (1 year of sessions)

    constfeat : bool
        If true, returned dataframe will include as first column
        the constant feature 1. Defaults to True.

    Returns
    --
    out : tuple (DataFrame, DataFrame)
        features and labels derived from the given parameters.
    """
    pricecol = kwargs.get('pricecol', 'Adj Close')
    averaging_interval = kwargs.get('averaging_interval', 252)
    labels, skipatend = labelfunc(eqdata.iloc[(n_sessions + averaging_interval - 1):, :], pricecol)
    growth = get_growth(eqdata, selection=pricecol, 
            skipstartrows=(averaging_interval - 1), skipendrows=skipatend)
    volume = _get_ratio_to_ave(eqdata, averaging_interval, skipendrows=skipatend)
    features = _featurize_growth_vol(growth, volume, n_sessions)
    if kwargs.get('constfeat', True):
        features = add_const(features)
    return features, labels

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

def _get_ratio_to_ave(eqdata, averaging_interval, **kwargs):
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
