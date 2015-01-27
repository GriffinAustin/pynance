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

from __future__ import absolute_import
from functools import partial

import numpy as np
import pandas as pd

from .. import common
from .. import tech

def growth_vol(n_sessions, eqdata, **kwargs):
    """
    Derive growth and relative volume data from `eqdata` and
    combine into a set of features.

    Using partial to fix `n_sessions` or keyword arguments,
    this function can be passed as `featurefunc` to `data.labeledfeatures()`.

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
    _growth = tech.growth(eqdata, selection=_pricecol, skipstartrows=(_averaging_interval - 1),
        skipendrows=_skipatend)
    _vol = tech.ratio_to_ave(eqdata, _averaging_interval, skipendrows=_skipatend)
    _features = _featurize_growth_vol(_growth, _vol, n_sessions) 
    if kwargs.get('constfeat', True):
        _features = add_const(_features)
    return _features, _skipatstart

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
    growth_feat = common.featurize(growth, n_sessions, selection='Growth')
    vol_feat = common.featurize(volume, n_sessions, selection='Rel Vol')
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
