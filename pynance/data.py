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

def featurize(equity_data, n_sessions, col_label='Adj Close', verbose=True):
    """
    Generate a raw (unnormalized) feature set from the input data.
    The value at col_label on the given date is taken
    as a feature, and each row contains values for n_sessions
    """
    features = pd.DataFrame(index=equity_data.index[(n_sessions - 1):],
            columns=range((-n_sessions + 1), 1))
    msg_freq = int(128 * 128 / n_sessions)
    # TODO vectorize or multi-thread
    # This is too slow for large data sets
    for i in range(len(features.index)):
        features.iloc[i, :] = equity_data[i:(n_sessions + i)][col_label].values
        if verbose and i % msg_freq == msg_freq - 1:
            print "Processing row {0}".format(i + 1)
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

    Notes
    ---
    If labels are real-valued, they should also be normalized.
    """
    norm = 1.0 if 'norm' not in kwargs else kwargs['norm']
    # http://stackoverflow.com/questions/18833639/attributeerror-in-python-numpy-when-constructing-function-for-certain-values
    if 'method' in kwargs and kwargs['method'] != "vector":
        # TODO test all of these
        if kwargs['method'] == "last":
            row_norms = features.loc[:, 0].values
        elif kwargs['method'] == "first":
            row_norms = features.iloc[:, 0].values
        elif kwargs['method'] == "mean":
            row_norms = np.mean(features.values, axis=1)
        else:
            raise ValueError("'{0}' not a valid normalization method".format(kwargs['method'])
    else:
        row_norms = np.linalg.norm(np.float64(features.values), axis=1)
    if 'labels' in kwargs:
        return features.apply(lambda col: col * norm / row_norms, axis=0), \
                kwargs['labels'].apply(lambda col: col * norm / row_norms, axis=0)
    else:
        return features.apply(lambda col: col * norm / row_norms, axis=0)

