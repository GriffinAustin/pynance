"""
.. Copyright (c) 2014 Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - building features (:mod:`pynance.data.feat`)
==============================================================

.. currentmodule:: pynance.data.feat

These functions are intended to be used in conjunction
with `functools.partial` and other function decorators
to pass to `data.labeledfeatures()`.
For example,

>>> from functools import partial
>>> featfunc = pn.decorate(partial(pn.data.feat.fromfuncs, [fn1, fn2, fn3], skipatstart=averaging_window), 
        averaging_window + n_feature_sessions - 1)
>>> features, labels = pn.data.labeledfeatures(eqdata, featfunc, labelfunc) 
"""

from functools import partial

import numpy as np
import pandas as pd

def add_const(features):
    """
    Prepend the constant feature 1 as first feature and return the modified
    feature set.

    Parameters
    ----------
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

def fromcols(selection, n_sessions, eqdata, **kwargs):
    """
    Generate features from selected columns of a dataframe.

    Parameters
    ----------
    selection : list or tuple of str
        Columns to be used as features.

    n_sessions : int
        Number of sessions over which to create features.

    eqdata : DataFrame
        Data from which to generate feature set. Must contain
        as columns the values from which the features are to
        be generated.

    constfeat : bool, optional
        Whether or not the returned features will have the constant
        feature.

    Returns
    ----------
    features : DataFrame
    """
    _constfeat = kwargs.get('constfeat', True)
    _outcols = ['Constant'] if _constfeat else []
    _n_rows = len(eqdata.index)
    for _col in selection:
        _outcols += map(partial(_concat, strval=' ' + _col), range(-n_sessions + 1, 1))
    _features = pd.DataFrame(index=eqdata.index[n_sessions - 1:], columns=_outcols, dtype=np.float64)
    _offset = 0
    if _constfeat:
        _features.iloc[:, 0] = 1.
        _offset += 1
    for _col in selection:
        _values = eqdata.loc[:, _col].values
        for i in range(n_sessions):
            _features.iloc[:, _offset + i] = _values[i:_n_rows - n_sessions + i + 1]
        _offset += n_sessions
    return _features

def fromfuncs(funcs, n_sessions, eqdata, **kwargs):
    """
    Generate features using a list of functions to apply to input data

    Parameters
    ----------
    funcs : list of function
        Functions to apply to eqdata. Each function is expected
        to output a dataframe with index identical to a slice of `eqdata`.
        The slice must include at least `eqdata.index[skipatstart + n_sessions - 1:]`.
        Each function is also expected to have a function attribute
        `title`, which is used to generate the column names of the
        output features.

    n_sessions : int
        Number of sessions over which to create features.

    eqdata : DataFrame
        Data from which to generate features. The data will often
        be retrieved using `pn.get()`.

    constfeat : bool, optional
        Whether or not the returned features will have the constant
        feature.

    skipatstart : int, optional
        Number of rows to omit at the start of the output DataFrame.
        This parameter is necessary if any of the functions requires
        a rampup period before returning valid results, e.g. `sma()` or
        functions calculating volume relative to a past baseline.
        Defaults to 0.

    Returns
    ----------
    features : DataFrame
    """
    _skipatstart = kwargs.get('skipatstart', 0)
    _constfeat = kwargs.get('constfeat', True)
    _outcols = ['Constant'] if _constfeat else []
    _n_allrows = len(eqdata.index)
    _n_featrows = _n_allrows - _skipatstart - n_sessions + 1
    for _func in funcs:
        _outcols += map(partial(_concat, strval=' ' + _func.title), range(-n_sessions + 1, 1))
    _features = pd.DataFrame(index=eqdata.index[_skipatstart + n_sessions - 1:],
            columns=_outcols, dtype=np.float64)
    _offset = 0
    if _constfeat:
        _features.iloc[:, 0] = 1.
        _offset += 1
    for _func in funcs:
        _values = _func(eqdata).values
        _n_values = len(_values)
        for i in range(n_sessions):
            _val_end = _n_values - n_sessions + i + 1
            _features.iloc[:, _offset + i] = _values[_val_end - _n_featrows:_val_end]
        _offset += n_sessions
    return _features

def _concat(intval, strval):
    return str(intval) + strval
