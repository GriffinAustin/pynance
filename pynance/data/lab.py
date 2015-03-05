"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - building labels (:mod:`pynance.data.lab`)
====================================================

.. currentmodule:: pynance.data.lab

These functions are intended to be used in conjunction
with :func:`functools.partial` to pass to 
:func:`pynance.data.combine.labeledfeatures`.
For example::

    >>> from functools import partial
    >>> features, labels = pn.data.labeledfeatures(eqdata, 256,
    ...        partial(pn.data.lab.growth, 32))
"""

import pandas as pd

def growth(interval, pricecol, eqdata):
    """
    Retrieve growth labels.

    Parameters
    --------------
    interval : int
        Number of sessions over which growth is measured. For example, if
        the value of 32 is passed for `interval`, the data returned will 
        show the growth 32 sessions ahead for each data point.
    eqdata : DataFrame
        Data for evaluating growth.
    pricecol : str
        Column of `eqdata` to be used for prices (Normally 'Adj Close').

    Returns
    --------
    labels : DataFrame
        Growth labels for the specified period
    skipatend : int
        Number of rows skipped at the end of `eqdata` for the given labels.
        Used to synchronize labels and features.

    Examples
    ---------------
    >>> from functools import partial
    >>> features, labels = pn.data.labeledfeatures(eqdata, 256, 
    ...        partial(pn.data.lab.growth, 32, 'Adj Close'))
    """
    size = len(eqdata.index)
    labeldata = eqdata.loc[:, pricecol].values[interval:] /\
            eqdata.loc[:, pricecol].values[:(size - interval)]
    df = pd.DataFrame(data=labeldata, index=eqdata.index[:(size - interval)],
            columns=['Growth'], dtype='float64')
    return df
