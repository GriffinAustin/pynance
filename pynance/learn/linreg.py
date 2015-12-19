"""
.. Copyright (c) 2014, 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Linear regression (:mod:`pynance.learn.linreg`)
===============================================

.. currentmodule:: pynance.learn.linreg
"""

def run(features, labels, lamb=0., constfeat=True):
    """
    Run linear regression on the given data.

    Parameters
    ----------
    features : DataFrame
        Features on which to run linear regression.

    labels : DataFrame
        Labels for the given features. Multiple columns
        of labels are allowed.

    lamb : float, optional
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
    feat = features.values
    lab = labels.values
    n_col = (feat.shape[1] if len(feat.shape > 1) else 1)
    reg_matrix = lamb * np.identity(n_col, dtype='float64')
    if constfeat:
        reg_matrix[0, 0] = 0.
    return np.linalg.lstsq(feat.T.dot(feat) + reg_matrix, feat.T.dot(lab))[0]
