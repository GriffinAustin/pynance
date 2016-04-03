"""
.. Copyright (c) 2014-2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Portfolio optimization (:mod:`pynance.pf`)
==========================================

.. currentmodule:: pynance.pf
"""

import numpy as np

def optimize(exp_rets, covs):
    """
    Return parameters for portfolio optimization.

    Parameters
    ----------
    exp_rets : ndarray
        Vector of expected returns for each investment..
    covs : ndarray
        Covariance matrix for the given investments.

    Returns
    ---------
    a : ndarray
        The first vector (to be combined with target return as scalar)
        in the linear equation for optimal weights.
    b : ndarray
        The second (constant) vector in the linear equation for
        optimal weights.
    least_risk_ret : int
        The return achieved on the portfolio that combines the given
        equities so as to achieve the lowest possible risk.

    Notes
    ---------
    *   The length of `exp_rets` must match the number of rows
        and columns in the `covs` matrix.
    *   The weights for an optimal portfolio with expected return
        `ret` is given by the formula `w = ret * a + b` where `a`
        and `b` are the vectors returned here. The weights `w` for
        the portfolio with lowest risk are given by `w = least_risk_ret * a + b`.
    *   An exception will be raised if the covariance matrix
        is singular or if each prospective investment has the
        same expected return.
    """
    _cov_inv = np.linalg.inv(covs)        

    # unit vector
    _u = np.ones((len(exp_rets)))

    # compute some dot products one time only
    _u_cov_inv = _u.dot(_cov_inv)
    _rets_cov_inv = exp_rets.dot(_cov_inv)

    # helper matrix for deriving Lagrange multipliers
    _m = np.empty((2, 2))
    _m[0, 0] = _rets_cov_inv.dot(exp_rets)
    _m[0, 1] = _u_cov_inv.dot(exp_rets)
    _m[1, 0] = _rets_cov_inv.dot(_u)
    _m[1, 1] = _u_cov_inv.dot(_u)

    # compute values to return
    _m_inv = np.linalg.inv(_m)
    a = _m_inv[0, 0] * _rets_cov_inv + _m_inv[1, 0] * _u_cov_inv
    b = _m_inv[0, 1] * _rets_cov_inv + _m_inv[1, 1] * _u_cov_inv
    least_risk_ret = _m[0, 1] / _m[1, 1]
    return a, b, least_risk_ret
