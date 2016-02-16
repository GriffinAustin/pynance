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

    .. versionadded:: 0.5.0

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
    return np.average(diff * diff, axis=0)

def stderr(predicted, actual):
    """
    Standard error of predictions.

    .. versionadded:: 0.5.0

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

