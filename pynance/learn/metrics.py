"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Metrics (:mod:`pynance.learn.metrics`)
===============================================

.. currentmodule:: pynance.learn.metrics
"""

import numpy as np

def mse(predicted, actual):
    """
    Mean squared error of predictions.

    Parameters
    ----------
    predicted : ndarray
        Predictions on which to measure error. May
        contain a single or multiple column but must
        match `actual` in shape.

    actual : ndarray
        Actual values against which to measure predictions.

    Returns
    -------
    err : ndarray
        Mean squared error of predictions relative to actual
        values.
    """
    diff = predicted - actual
    ncols = (diff.shape[1] if len(diff.shape) > 1 else 1) 
    return np.average(diff * diff, axis=0).reshape(1, ncols)

def stderr(predicted, actual):
    """
    Standard error of predictions.

    Parameters
    ----------
    predicted : ndarray
        Predictions on which to measure error. May
        contain a single or multiple column but must
        match `actual` in shape.

    actual : ndarray
        Actual values against which to measure predictions.

    Returns
    -------
    err : ndarray
        Standard error of predictions relative to actual
        values.
    """
    return np.sqrt(mse(predicted, actual))

