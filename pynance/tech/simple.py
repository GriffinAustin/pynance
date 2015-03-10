"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Technical analysis - basic metrics (:mod:`pynance.tech.simple`)
==================================================================

.. currentmodule:: pynance.tech.simple
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

def growth(eqdata, **kwargs):
    """
    Generate a DataFrame where the sole column, 'Growth',
    is the growth for the equity over the given number of sessions.
    
    For example, if 'XYZ' has 'Adj Close' of `100.0` on 2014-12-15 and 
    `90.0` 4 *sessions* later on 2014-12-19, then the 'Growth' value
    for 2014-12-19 will be `0.9`.

    Parameters
    ----------
    eqdata : DataFrame
        Data such as that returned by :func:`pynance.data.retrieve.get`
    selection : str, optional
        Column from which to determine growth values. Defaults to
        'Adj Close'.
    n_sessions : int
        Number of sessions to count back for calculating today's
        growth. For example, if `n_sessions` is set to 4, growth is
        calculated relative to the price 4 sessions ago. Defaults
        to 1 (price of previous session).
    skipstartrows : int
        Rows to skip at beginning of `eqdata` in addition to the 1 row that must
        be skipped because the calculation relies on a prior data point.
        Defaults to 0.
    skipendrows : int
        Rows to skip at end of `eqdata`. Defaults to 0.
    outputcol : str, optional
        Name to use for output column. Defaults to 'Growth'

    Returns
    ----------
    out : DataFrame

    Notes
    ----------
    The interval is the number of *sessions* between the 2 values
    whose ratio is being measured, *not* the number of days (which
    includes days on which the market is closed).

    Growth is measured relative to the earlier
    date, but the index date is the later date. This index is chosen because
    it is the date on which the value is known.
    """
    selection = kwargs.get('selection', 'Adj Close')
    n_sessions = kwargs.get('n_sessions', 1)
    skipstartrows = kwargs.get('skipstartrows', 0)
    skipendrows = kwargs.get('skipendrows', 0)
    outputcol = kwargs.get('outputcol', 'Growth')
    size = len(eqdata.index)
    growthdata = eqdata.loc[:, selection].values[(skipstartrows + n_sessions):(size - skipendrows)] / \
            eqdata.loc[:, selection].values[skipstartrows:(-n_sessions - skipendrows)]
    growthindex = eqdata.index[(skipstartrows + n_sessions):(size - skipendrows)]
    return pd.DataFrame(data=growthdata, index=growthindex, columns=[outputcol], dtype='float64')

def ln_growth(eqdata, **kwargs):
    """
    Return the natural log of growth.

    See also
    --------
    :func:`growth`
    """
    if 'outputcol' not in kwargs:
        kwargs['outputcol'] = 'LnGrowth'
    return np.log(growth(eqdata, **kwargs))

def ret(eqdata, **kwargs):
    """
    Generate a DataFrame where the sole column, 'Return',
    is the return for the equity over the given number of sessions.
    
    For example, if 'XYZ' has 'Adj Close' of `100.0` on 2014-12-15 and 
    `90.0` 4 *sessions* later on 2014-12-19, then the 'Return' value
    for 2014-12-19 will be `-0.1`.

    Parameters
    ----------
    eqdata : DataFrame
        Data such as that returned by `get()`
    selection : str, optional
        Column from which to determine growth values. Defaults to
        'Adj Close'.
    n_sessions : int
        Number of sessions to count back for calculating today's
        return. For example, if `n_sessions` is set to 4, return is
        calculated relative to the price 4 sessions ago. Defaults
        to 1 (price of previous session).
    skipstartrows : int
        Rows to skip at beginning of `eqdata` in addition to the 1 row that must
        be skipped because the calculation relies on a prior data point.
        Defaults to 0.
    skipendrows : int
        Rows to skip at end of `eqdata`. Defaults to 0.
    outputcol : str, optional
        Name for column of output dataframe. Defaults to 'Return'.

    Returns
    ----------
    out : DataFrame

    See Also
    --------
    :func:`growth`

    Notes
    ----------
    The interval is the number of *sessions* between the 2 values
    whose ratio is being measured, *not* the number of days (which
    includes days on which the market is closed).

    The percentage gain or loss is measured relative to the earlier
    date, but the index date is the later date. The index is chose because
    that is the date on which the value is known. The percentage measure is because
    that is the way for calculating percent profit and loss.
    """
    if 'outputcol' not in kwargs:
        kwargs['outputcol'] = 'Return'
    result = growth(eqdata, **kwargs)
    result.values[:, :] -= 1.
    return result
