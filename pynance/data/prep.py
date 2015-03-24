"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - preprocessing functions (:mod:`pynance.data.prep`)
=========================================================

.. currentmodule:: pynance.data.prep
"""

import numpy as np
import pandas as pd

def center(dataset, out=None):
    """
    Returns a centered data set.
    
    Each column of the returned data will have mean 0.
    The row vector subtracted from each row to achieve this
    transformation is also returned.

    Parameters
    ----------
    dataset : DataFrame or ndarray

    out : DataFrame or ndarray, optional
        Alternate output array in which to place the result.
        If provided, it must have the same shape and type
        (DataFrame or ndarray) as the expected output.

    Returns
    ----------
    out : tuple of DataFrame or ndarray
        The output data is of the same type as the input.

    Notes
    ----------
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
    ----------
    centered_data : DataFrame or ndarray

    out : DataFrame or ndarray, optional
        Alternate output array in which to place the result.
        If provided, it must have the same shape and type
        (DataFrame or ndarray) as the expected output.

    Returns
    ----------
    out : tuple of DataFrame or ndarray
        The output data is of the same type as the input.

    Notes
    ----------
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
    Return a transformed DataFrame.

    Transform data_frame along the given axis. By default, each row will be normalized (axis=0).

    Parameters
    -----------
    data_frame : DataFrame
        Data to be normalized.
    axis : int, optional
        0 (default) to normalize each row, 1 to normalize each column.
    method : str, optional
        Valid methods are:
        
        -  "vector" : Default for normalization by row (axis=0).
           Normalize along axis as a vector with norm `norm`
        -  "last" : Linear normalization setting last value along the axis to `norm`
        -  "first" : Default for normalization of columns (axis=1).
           Linear normalization setting first value along the given axis to `norm`
        -  "mean" : Normalize so that the mean of each vector along the given axis is `norm`
    norm : float, optional
        Target value of normalization, defaults to 1.0.
    labels : DataFrame, optional
        Labels may be passed as keyword argument, in which
        case the label values will also be normalized and returned.

    Returns
    -----------
    df : DataFrame
        Normalized data.
    labels : DataFrame, optional
        Normalized labels, if provided as input.

    Notes
    -----------
    If labels are real-valued, they should also be normalized.

    ..
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
