"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - compare (:mod:`pynance.data.compare`)
=================================================

.. currentmodule:: pynance.data.compare
"""

import numpy as np
import pandas as pd

def compare(eq_dfs, columns=None, selection='Close'):
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
    selection : str, default 'Close'
        Column containing prices to be compared. Defaults
        to 'Close'.

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
        rel_perf = pn.data.compare(eq_dfs, eqs)

    Notes
    -----
    Each set of data passed in `eq_dfs` is assumed to have
    the same start and end dates as the other data sets.
    """
    content = np.empty((eq_dfs[0].shape[0], len(eq_dfs)), dtype=np.float64)
    rel_perf = pd.DataFrame(content, eq_dfs[0].index, columns, dtype=np.float64)
    for i in range(len(eq_dfs)):
        rel_perf.iloc[:, i] = eq_dfs[i].loc[:, selection] / eq_dfs[i].iloc[0].loc[selection]
    return rel_perf
