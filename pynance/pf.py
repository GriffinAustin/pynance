"""
.. Copyright (c) 2014, 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Performance (:mod:`pynance.pf`)
===============================

.. currentmodule:: pynance.pf
"""

import numpy as np
import pandas as pd

def get_relative(eq_dfs, columns=None, selection='Adj Close'):
    """
    Get the relative performance of multiple equities.

    .. versionadded:: 0.5.0

    Parameters
    ----------
    eq_dfs : list or tuple of DataFrame
        Performance data for multiple equities over
        a consistent time frame.
    columns : iterable of str, default None
        Labels to use for the columns of the output DataFrame.
        The labels, if provided, should normally be the names
        of the equities whose performance is being compared.
    selection : str, default 'Adj Close'
        Column containing prices to be compared. Defaults
        to 'Adj Close'.

    Returns
    -------
    rel_perf : DataFrame
        A DataFrame whose columns contain normalized data
        for each equity represented in `eq_dfs`. The initial
        price for each equity will be normalized to 1.0.

    Examples
    --------

    .. code-block:: python

        import pynance as pn

        eqs = ('FSLR', 'SCTY', 'SPWR')
        eq_dfs = []
        for eq in eqs:
            eq_dfs.append(pn.data.get(eq, '2016'))
        rel_perf = pn.pf.get_relative(eq_dfs, eqs)

    Notes
    -----
    The indices for each set of data passed in `eq_dfs` are assumed to have
    the same start and end dates.
    """
    content = np.empty((eq_dfs[0].shape[0], len(eq_dfs)), dtype=np.float64)
    rel_perf = pd.DataFrame(content, eq_dfs[0].index, columns, dtype=np.float64)
    for i in range(len(eq_dfs)):
        rel_perf.iloc[:, i] = eq_dfs[i].loc[:, selection] / eq_dfs[i].iloc[0].loc[selection]
    return rel_perf

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
