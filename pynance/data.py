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
    equity_data : DataFrame from which to generate features

    n_sessions : number of sessions to use as features

    **kwargs :
        selection : column of `equity_data` from which to generate
        features. Defaults to 'Adj Close'.

        columns : list of column names in output DataFrame.
        Defaults to map(str, range((-n_sessions + 1), 1)), e.g.
        ['-5', '-4', '-3', '-2', '-1', '0']

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

def normalize(data_frame, **kwargs):
    """
    normalize(data_frame, **kwargs)

    Normalize data_frame along the given axis. By default, each row
    will be normalized (axis=0)

    Parameters
    ---
    data_frame : data_frame to be normalized

    **kwargs :
        axis : 0 (default) to normalize each row, 1 to normalize each column
        method : valid methods are
            "vector" : Default for normalization by row (axis=0).
            Normalize along axis as a vector with norm `norm`
            "last" : Linear normalization setting last value along the axis to `norm`
            "first" : Default for normalization of columns (axis=1).
            Linear normalization setting first value along the given axis to `norm`
            "mean" : Normalize so that the mean of each vector along the given axis is `norm`

        norm : Defaults to 1.0. Target value of normalization.

        labels : labels may be passed as keyword argument, in which
            case the label values will be normalized and returned

    Return
    ---
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
