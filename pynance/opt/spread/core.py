"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - spreads (:mod:`pynance.opt.spread.core`)
==================================================

.. currentmodule:: pynance.opt.spread.core
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from .._common import _relevant_rows
from .._common import _getprice
from .multi import Multi
from .vert import Vertical

class Spread(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on options spreads.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data
    multi
    vert
    """
    def __init__(self, df):
        self.data = df
        self.vert = Vertical(df)
        self.multi = Multi(df)

    def cal(self, opttype, strike, exp1, exp2):
        """
        Metrics for evaluating a calendar spread.

        Parameters
        ------------
        opttype : str ('call' or 'put')
            Type of option on which to collect data.
        strike : numeric
            Strike price.
        exp1 : date or date str (e.g. '2015-01-01')
            Earlier expiration date.
        exp2 : date or date str (e.g. '2015-01-01')
            Later expiration date.

        Returns
        ------------
        metrics : DataFrame
            Metrics for evaluating spread.
        """
        _row1 = _relevant_rows(self.data, (strike, exp1, opttype,),
                "No key for {} strike {} {}".format(exp1, strike, opttype))
        _row2 = _relevant_rows(self.data, (strike, exp2, opttype,),
                "No key for {} strike {} {}".format(exp2, strike, opttype))
        _price1 = _getprice(_row1)
        _price2 = _getprice(_row2)
        _eq = _row1.loc[:, 'Underlying_Price'].values[0]
        _qt = _row1.loc[:, 'Quote_Time'].values[0]
        _index = ['Near', 'Far', 'Debit', 'Underlying_Price', 'Quote_Time']
        _vals = np.array([_price1, _price2, _price2 - _price1, _eq, _qt])
        return pd.DataFrame(_vals, index=_index, columns=['Value'])
