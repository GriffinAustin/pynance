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

def normalize(features, **kwargs):
    """
    normalize(features, **kwargs)

    Normalize features by row. Labels may optionally be normalized if
    they are passed as keyword arguemnt

    Parameters
    ---
    features : features to be normalized

    **kwargs :
        method : valid methods are
            "vector" : Default, normalize as a vector with norm `norm`
            "last" : Linear normalization setting last feature value to `norm`
            "first" : Linear normalization setting first feature value to `norm`
            "mean" : Normalize so that the mean of each row is `norm`

        norm : Defaults to 1.0. Target value of normalization.

        labels : labels may be passed as keyword argument, in which
            case the label values will be normalized and returned

    Return
    ---
    Normalized features if no labels are provided. Otherwise, a tuple
    containing first normalized features, then normalized labels.

    Notes
    ---
    If labels are real-valued, they should also be normalized.

    Having row_norms as a numpy array should be benchmarked against 
    using a DataFrame:
    http://stackoverflow.com/questions/12525722/normalize-data-in-pandas
    Note: This isn't a bottleneck. Using a feature set with 13k rows and 256
    features ('ge' from 1962 until now), the normalization was immediate.
    """
    norm = kwargs.get('norm', 1.0)
    method = kwargs.get('method', 'vector')
    if method == 'vector':
        row_norms = np.linalg.norm(features.values, axis=1)
    elif method == 'last':
        row_norms = features.iloc[:, -1].values
    elif method == 'mean':
        row_norms = np.mean(features.values, axis=1)
    elif method == 'first':
        row_norms = features.iloc[:, 0].values
    else:
        raise ValueError("no normalization method '{0}'".format(method))
    if 'labels' in kwargs:
        return features.apply(lambda col: col * norm / row_norms, axis=0), \
                kwargs['labels'].apply(lambda col: col * norm / row_norms, axis=0)
    else:
        return features.apply(lambda col: col * norm / row_norms, axis=0)
