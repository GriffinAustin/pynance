"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - vertical spreads (:mod:`pynance.opt.spread.vert`)
==================================================

.. currentmodule:: pynance.opt.spread.vert
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from .._common import _relevant_rows
from .._common import _getprice
from .. import _constants


class Vertical(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on vertical options spreads

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data
    """
    def __init__(self, df):
        self.data = df

    def straddle(self, strike, expiry):
        """
        Metrics for evaluating a straddle

        Parameters
        ------------
        strike : numeric
            Strike price.
        expiry : date or date str (e.g. '2015-01-01')
            Expiration date.

        Returns
        ------------
        metrics : DataFrame
            Metrics for evaluating straddle.
        """
        _rows = {}
        _prices = {}
        for _opttype in _constants.OPTTYPES:
            _rows[_opttype] = _relevant_rows(self.data, (strike, expiry, _opttype,),
                    "No key for {} strike {} {}".format(expiry, strike, _opttype))
            _prices[_opttype] = _getprice(_rows[_opttype])
        _eq = _rows[_constants.OPTTYPES[0]].loc[:, 'Underlying_Price'].values[0]
        _qt = _rows[_constants.OPTTYPES[0]].loc[:, 'Quote_Time'].values[0]
        _index = ['Call', 'Put', 'Credit', 'Underlying_Price', 'Quote_Time']
        _vals = np.array([_prices['call'], _prices['put'], _prices['call'] + _prices['put'], _eq, _qt])
        return pd.DataFrame(_vals, index=_index, columns=['Value'])
