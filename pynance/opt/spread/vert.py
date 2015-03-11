"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - vertical spreads (:mod:`pynance.opt.spread.vert`)
===========================================================

.. currentmodule:: pynance.opt.spread.vert
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from .._common import _relevant_rows
from .._common import _getprice
from .. import _constants


class Vert(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on vertical options spreads

    Objects of this class are not intended for direct instantiation
    but are created as attributes of objects of type 
    :class:`~pynance.opt.spread.core.Spread`.

    .. versionadded:: 0.3.0

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data : :class:`pandas.DataFrame`

    Methods
    -------
    .. automethod:: call

    .. automethod:: put

    .. automethod:: straddle
    """
    def __init__(self, df):
        self.data = df

    def call(self, lowstrike, highstrike, expiry):
        """
        Metrics for evaluating a bull call spread.
        
        The metrics returned can easily be translated into bear
        spread metrics. The difference is only whether one buys
        the call at the lower strike and sells at the higher
        (bull call spread) or sells at the lower while buying
        at the higher (bear call spread). The metrics
        dataframe shows values for a bull call spread, where
        the transaction is a debit. A bear call spread
        is created by *selling* a bull call spread, so the transaction
        amount is the same, but it
        is a credit rather than a debit.

        Parameters
        ------------
        lowstrike : numeric
            Lower strike price.
        highstrike : numeric
            Higher strike sprice.
        expiry : date or date str (e.g. '2015-01-01')
            Expiration date.

        Returns
        ------------
        metrics : DataFrame

        Notes
        -----
        Cf. Lawrence McMillan, Options as a Strategic Investment, 5th ed., pp. 157ff.

        See Also
        --------
        :meth:`put`
        """
        _rows = {}
        _prices = {}
        _opttype = 'call'
        for _strike in (lowstrike, highstrike):
            _rows[_strike] = _relevant_rows(self.data, (_strike, expiry, _opttype,),
                    "No key for {} strike {} {}".format(expiry, _strike, _opttype))
            _prices[_strike] = _getprice(_rows[_strike])
        _eq = _rows[lowstrike].loc[:, 'Underlying_Price'].values[0]
        _qt = _rows[lowstrike].loc[:, 'Quote_Time'].values[0]
        _debit = _prices[lowstrike] - _prices[highstrike]
        _breakeven = lowstrike + _debit
        if _breakeven > highstrike:
            _breakeven = np.nan
        _maxprof = highstrike - lowstrike -_debit
        _index = ['Low Strike Call', 'High Strike Call', 'Debit',  'Break_Even',
                'Max Profit', 'Underlying_Price', 'Quote_Time']
        _vals = np.array([_prices[lowstrike], _prices[highstrike], _debit,
                _breakeven, _maxprof, _eq, _qt])
        return pd.DataFrame(_vals, index=_index, columns=['Value'])

    def put(self, lowstrike, highstrike, expiry):
        """
        Metrics for evaluating a bear put spread.
        
        The metrics returned can easily be translated into bull
        spread metrics. The difference is only whether one buys
        the put at the lower strike and sells at the higher
        (bear put spread) or sells at the lower while buying
        at the higher (bull put spread). The metrics
        dataframe shows values for a bear put spread, where
        the transaction is a debit. A bull put spread
        is created by *selling* a bear put spread, so the transaction
        amount is the same, but it
        is a credit rather than a debit.

        Parameters
        ------------
        lowstrike : numeric
            Lower strike price.
        highstrike : numeric
            Higher strike sprice.
        expiry : date or date str (e.g. '2015-01-01')
            Expiration date.

        Returns
        ------------
        metrics : DataFrame

        Notes
        -----
        Cf. Lawrence McMillan, Options as a Strategic Investment, 5th ed., pp. 316ff.

        See Also
        --------
        :meth:`call`
        """
        _rows = {}
        _prices = {}
        _opttype = 'put'
        for _strike in (lowstrike, highstrike):
            _rows[_strike] = _relevant_rows(self.data, (_strike, expiry, _opttype,),
                    "No key for {} strike {} {}".format(expiry, _strike, _opttype))
            _prices[_strike] = _getprice(_rows[_strike])
        _eq = _rows[lowstrike].loc[:, 'Underlying_Price'].values[0]
        _qt = _rows[lowstrike].loc[:, 'Quote_Time'].values[0]
        _debit = _prices[highstrike] - _prices[lowstrike]
        _breakeven = highstrike - _debit
        _maxprof = highstrike - lowstrike -_debit
        if _breakeven < lowstrike:
            _breakeven = np.nan
        _index = ['Low Strike Put', 'High Strike Put', 'Debit',  'Break_Even',
                'Max Profit', 'Underlying_Price', 'Quote_Time']
        _vals = np.array([_prices[lowstrike], _prices[highstrike], _debit,
                _breakeven, _maxprof, _eq, _qt])
        return pd.DataFrame(_vals, index=_index, columns=['Value'])

    def straddle(self, strike, expiry):
        """
        Metrics for evaluating a straddle.

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
