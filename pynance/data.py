"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Data retrieval
Wraps Pandas Remote Data Access: 
http://pandas.pydata.org/pandas-docs/stable/remote_data.html
"""

import numpy as np
import pandas as pd
import pandas.io.data as web

def get(equity, start, end):
    """ Get DataFrame for an individual equity from Yahoo!  """
    return web.DataReader(equity, 'yahoo', start, end)

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

def center(dataset, out=None):
    """
    Returns a centered data set.
    
    Each column of the returned data will have mean 0.
    The row vector subtracted from each row to achieve this
    transformation is also returned.

    Parameters
    --
    dataset : DataFrame or ndarray

    out : DataFrame or ndarray, optional
        Alternate output array in which to place the result.
        If provided, it must have the same shape and type
        (DataFrame or ndarray) as the expected output.

    Returns
    --
    out : tuple of DataFrame or ndarray
        The output data is of the same type as the input.

    Notes
    --
    To exclude a column (such as a constant feature, which is
    usually the first or last column of data) simply don't
    include it in the input. For example:

    >>> centered_data, means = pn.center(mydata.iloc[:, 1:])

    To perform this operation in place:

    >>> _, means = pn.center(mydata.iloc[:, 1:], out=mydata.iloc:, 1:])
    """
    return _preprocess(_center_fn, dataset, out)

def _preprocess(func, dataset, out):
    # Generic preprocessing function used in center() and normalize()
    is_df = isinstance(dataset, pd.DataFrame)
    _data = (dataset.values if is_df else dataset)
    processed_data, adjustment = func(_data)
    if not is_df:
        if out is not None:
            out[:, :] = processed_data
            return out, adjustment
        return processed_data, adjustment
    adj_df = pd.DataFrame(data=adjustment, index=['Mean'], columns=dataset.columns,
            dtype='float64')
    if out is not None:
        out.values[:, :] = processed_data
        return out, adj_df
    processed_df = pd.DataFrame(data=processed_data, index=dataset.index, 
            columns=dataset.columns, dtype='float64')
    return processed_df, adj_df

def _center_fn(_data):
    adjustment = np.mean(_data, axis=0, dtype=np.float64).reshape((1, _data.shape[1]))
    centered_data = _data - adjustment
    return centered_data, adjustment

def _normalize_fn(_data):
    adjustment = np.std(_data, axis=0, dtype=np.float64).reshape((1, _data.shape[1]))
    normalized_data = _data / adjustment
    return normalized_data, adjustment

def normalize(centered_data, out=None):
    """
    Returns a data set with standard deviation of 1.

    The input data must be centered for the operation to
    yield valid results: The mean of each column must be 0.
    Each column of the returned data set will have standard
    deviation 1.

    The row vector by which each row of data is divided is
    also returned.

    Parameters
    --
    centered_data : DataFrame or ndarray

    out : DataFrame or ndarray, optional
        Alternate output array in which to place the result.
        If provided, it must have the same shape and type
        (DataFrame or ndarray) as the expected output.

    Returns
    --
    out : tuple of DataFrame or ndarray
        The output data is of the same type as the input.

    Notes
    --
    To exclude a column (such as a constant feature, which is
    usually the first or last column of data) simply don't
    include it in the input. For example:

    >>> normalized_data, sd_adj = pn.normalize(mydata.iloc[:, 1:])

    To perform this operation in place:

    >>> _, sd_adj = pn.normalize(mydata.iloc[:, 1:], out=mydata.iloc:, 1:])
    """
    return _preprocess(_normalize_fn, centered_data, out)

def transform(data_frame, **kwargs):
    """
    Return a transformed DataFrame

    Transform data_frame along the given axis. By default, each row
    will be normalized (axis=0)

    Parameters
    ---
    data_frame : DataFrame
        data to be normalized

    axis : int in {0, 1}, default: 0
        0 to normalize each row, 1 to normalize each column
    method : str
        valid methods are
        - "vector" : Default for normalization by row (axis=0).
            Normalize along axis as a vector with norm `norm`
        - "last" : Linear normalization setting last value along the axis to `norm`
        - "first" : Default for normalization of columns (axis=1).
            Linear normalization setting first value along the given axis to `norm`
        - "mean" : Normalize so that the mean of each vector along the given axis is `norm`

    norm : float, default 1.0
        Target value of normalization.

    labels : DataFrame
        labels may be passed as keyword argument, in which
        case the label values will also be normalized and returned

    Returns
    ---
    out : DataFrame or tuple of 2 DataFrames
    
    Normalized data_frame if no labels are provided. Otherwise, a tuple
    containing first normalized data_frame, then normalized labels.

    Notes
    ---
    If labels are real-valued, they should also be normalized.

    Having row_norms as a numpy array should be benchmarked against 
    using a DataFrame:
    http://stackoverflow.com/questions/12525722/normalize-data-in-pandas
    Note: This isn't a bottleneck. Using a feature set with 13k rows and 256
    data_frame ('ge' from 1962 until now), the normalization was immediate.
    """
    norm = kwargs.get('norm', 1.0)
    axis = kwargs.get('axis', 0)
    if axis == 0:
        norm_vector = _get_norms_of_rows(data_frame, kwargs.get('method', 'vector'))
    else:
        norm_vector = _get_norms_of_cols(data_frame, kwargs.get('method', 'first'))

    if 'labels' in kwargs:
        if axis == 0:
            return data_frame.apply(lambda col: col * norm / norm_vector, axis=0), \
                    kwargs['labels'].apply(lambda col: col * norm / norm_vector, axis=0)
        else:
            raise ValueError("label normalization incompatible with normalization by column")
    else:
        if axis == 0:
            return data_frame.apply(lambda col: col * norm / norm_vector, axis=0)
        else:
            return data_frame.apply(lambda row: row * norm / norm_vector, axis=1)

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

def get_growth(eqdata, selection='Adj Close', n_sessions=1):
    """
    Generate a DataFrame where the sole column, 'Growth',
    is the growth for the equity over the given number of sessions.
    
    For example, if 'XYZ' has 'Adj Close' of `100.0` on 2014-12-15 and 
    `90.0` 4 *sessions* later on 2014-12-19, then the 'Growth' value
    for 2014-12-19 will be `0.9`.

    Notes
    --
    The interval is the number of *sessions* between the 2 values
    whose ratio is being measured, *not* the number of days (which
    includes days on which the market is closed).

    Growth is measured relative to the earlier
    date, but the index date is the later date. This index is chosen because
    it is the date on which the value is known.
    """
    result = pd.DataFrame(index=eqdata.index[n_sessions:], columns=['Growth'], dtype='float64')
    selected_data = eqdata.loc[:, selection]
    result.values[:, 0] = selected_data.values[n_sessions:] / selected_data.values[:-n_sessions]
    return result

def get_return(eqdata, selection='Adj Close', n_sessions=1):
    """
    Generate a DataFrame where the sole column, 'Return',
    is the return for the equity over the given number of sessions.
    
    For example, if 'XYZ' has 'Adj Close' of `100.0` on 2014-12-15 and 
    `90.0` 4 *sessions* later on 2014-12-19, then the 'Return' value
    for 2014-12-19 will be `-0.1`.

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
    result = pd.DataFrame(index=eqdata.index[n_sessions:], columns=['Return'], dtype='float64')
    selected_data = eqdata.loc[:, selection]
    result.values[:, 0] = selected_data.values[n_sessions:] / selected_data.values[:-n_sessions] - 1.
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
        take 3 arguments: `eqdata`, `n_sessions` and `pricecol`. The first
        2 arguments are those currently used. The 3rd argument is the label
        used for the desired price column (Typically 'Adj Close' or 'Close').
        `labelfunc` should return a dataframe of labels followed by an int
        specifying the number of feature rows to skip at the end of the feature
        dataframe. For example, if features are relative prices 64 days out,
        these features will only be known up until 64 days before the data
        runs out. In order to properly align features and labels, the features
        should not include the last 64 rows that would otherwise be possible.

        Usage:
        `labels, skipatend = labelfunc(eqdata, n_sessions, pricecol)`

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
    # TODO
    return None

def _get_norms_of_rows(data_frame, method):
    """ return a column vector containing the norm of each row """
    if method == 'vector':
        norm_vector = np.linalg.norm(data_frame.values, axis=1)
    elif method == 'last':
        norm_vector = data_frame.iloc[:, -1].values
    elif method == 'mean':
        norm_vector = np.mean(data_frame.values, axis=1)
    elif method == 'first':
        norm_vector = data_frame.iloc[:, 0].values
    else:
        raise ValueError("no normalization method '{0}'".format(method))
    return norm_vector

def _get_norms_of_cols(data_frame, method):
    """ return a row vector containing the norm of each column """
    if method == 'first':
        norm_vector = data_frame.iloc[0, :].values
    elif method == 'mean':
        norm_vector = np.mean(data_frame.values, axis=0)
    elif method == 'last':
        norm_vector = data_frame.iloc[-1, :].values
    elif method == 'vector':
        norm_vector = np.linalg.norm(data_frame.values, axis=0)
    else:
        raise ValueError("no normalization method '{0}'".format(method))
    return norm_vector
