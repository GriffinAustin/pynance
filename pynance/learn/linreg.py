"""
.. Copyright (c) 2014, 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Linear regression (:mod:`pynance.learn.linreg`)
===============================================

.. currentmodule:: pynance.learn.linreg
"""

import numpy as np

def run(features, labels, regul=0., constfeat=True):
    """
    Run linear regression on the given data.

    Parameters
    ----------
    features : ndarray
        Features on which to run linear regression.

    labels : ndarray
        Labels for the given features. Multiple columns
        of labels are allowed.

    regul : float, optional
        Regularization parameter. Defaults to 0.

    constfeat : bool, optional
        Whether or not the first column of features is
        the constant feature 1. If True, the first column
        will be excluded from regularization. Defaults to True.

    Returns
    -------
    model : ndarray
        Regression model for the given data.
    """
    n_col = (features.shape[1] if len(features.shape) > 1 else 1)
    reg_matrix = regul * np.identity(n_col, dtype='float64')
    if constfeat:
        reg_matrix[0, 0] = 0.
    return np.linalg.lstsq(features.T.dot(features) + reg_matrix, features.T.dot(labels))[0]

def predict(features, model):
    """
    Generate predictions from features and model.

    Parameters
    ----------
    features : ndarray
        Features from which to generate predictions

    model : ndarray
        Regression model.

    Returns
    -------
    predicted : ndarray
        Predictions generated from features using model.
    """
    return features.dot(model)
