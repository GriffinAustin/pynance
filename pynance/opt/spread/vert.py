"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - horizontal spreads (:mod:`pynance.opt.spread.horiz`)
==================================================

.. currentmodule:: pynance.opt.spread.horiz
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from .._common import _relevant_rows
from .._common import _getprice


class Horizontal(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on horizontal (calendar) spreads

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

    def cal(self, opttype, strike, exp1, exp2):
        """
        Metrics for evaluating a simple calendar spread.

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

def dblcal(optdata, lowstrike, highstrike, expiry1, expiry2):
    """
    Metrics for evaluating a double calendar spread.

    Parameters
    ------------
    optdata : DataFrame
        Data returned from :func:`pynance.opt.retrieve.get`
    opttype : str ('call' or 'put')
        Type of option on which to collect data.
    lowstrike : numeric
        Lower strike price. To be used for put spread.
    highstrike : numeric
        Higher strike price. To be used for call spread.
    expiry1 : date or date str (e.g. '2015-01-01')
        Earlier expiration date.
    expiry2 : date or date str (e.g. '2015-01-01')
        Later expiration date.

    Returns
    ------------
    metrics : DataFrame
        Metrics for evaluating spread.
    """
    _index = ['Near Call', 'Far Call', 'Call Ratio', 'Near Put', 'Far Put', 
            'Put Ratio', 'Near to Far Ratio', 'Debit', 'Underlying', 'Quote_Time']
    _metrics = pd.DataFrame(index=_index, columns=['Value'])
    _nearcall, _metrics.loc['Underlying', 'Value'], _metrics.loc['Quote_Time', 'Value'] =\
            price.get(optdata, 'call', highstrike, expiry1, False)
    _metrics.loc['Near Call', 'Value'] = _nearcall
    _farcall = price.get(optdata, 'call', highstrike, expiry2, False)[0]
    _metrics.loc['Far Call', 'Value'] = _farcall
    _metrics.loc['Call Ratio', 'Value'] = _nearcall / _farcall
    _nearput = price.get(optdata, 'put', lowstrike, expiry1, False)[0]
    _metrics.loc['Near Put', 'Value'] = _nearput
    _farput = price.get(optdata, 'put', lowstrike, expiry2, False)[0]
    _metrics.loc['Far Put', 'Value'] = _farput
    _metrics.loc['Put Ratio', 'Value'] = _nearput / _farput
    _metrics.loc['Near to Far Ratio', 'Value'] = (_nearcall + _nearput) / (_farcall + _farput)
    _metrics.loc['Debit', 'Value'] = _farcall + _farput - _nearcall - _nearput
    return _metrics

def diagbtrfly(optdata, lowstrike, midstrike, highstrike, expiry1, expiry2):
    """
    Metrics for evaluating a diagonal butterfly spread.

    Parameters
    ------------
    optdata : DataFrame
        Data returned from :func:`pynance.opt.retrieve.get`
    opttype : str ('call' or 'put')
        Type of option on which to collect data.
    lowstrike : numeric
        Lower strike price. To be used for far put.
    midstrike : numeric
        Middle strike price. To be used for near straddle.
        Typically at the money.
    highstrike : numeric
        Higher strike price. To be used for far call.
    expiry1 : date or date str (e.g. '2015-01-01')
        Earlier expiration date.
    expiry2 : date or date str (e.g. '2015-01-01')
        Later expiration date.

    Returns
    ------------
    metrics : DataFrame
        Metrics for evaluating spread.
    """
    _index = ['Straddle Call', 'Straddle Put', 'Straddle Total', 'Far Call', 'Far Put', 'Far Total',
            'Straddle to Far Ratio', 'Credit', 'Underlying', 'Quote_Time']
    _metrics = pd.DataFrame(index=_index, columns=['Value'])
    _straddlecall, _metrics.loc['Underlying', 'Value'], _metrics.loc['Quote_Time', 'Value'] =\
            price.get(optdata, 'call', midstrike, expiry1, False)
    _straddleput = price.get(optdata, 'put', midstrike, expiry1, False)[0]
    _farcall = price.get(optdata, 'call', highstrike, expiry2, False)[0]
    _farput = price.get(optdata, 'put', lowstrike, expiry2, False)[0]
    _metrics.loc['Straddle Call', 'Value'] = _straddlecall
    _metrics.loc['Straddle Put', 'Value'] = _straddleput
    _metrics.loc['Straddle Total', 'Value'] = _straddle_tot = _straddlecall + _straddleput
    _metrics.loc['Far Call', 'Value'] = _farcall
    _metrics.loc['Far Put', 'Value'] = _farput
    _metrics.loc['Far Total', 'Value'] = _far_tot = _farcall + _farput
    _metrics.loc['Straddle to Far Ratio', 'Value'] = _straddle_tot / _far_tot 
    _metrics.loc['Credit', 'Value'] = _straddle_tot - _far_tot
    return _metrics

def straddle(optdata, strike, expiry):
    """
    Metrics for evaluating a straddle

    Parameters
    ------------
    optdata : DataFrame
        Data returned from :func:`pynance.opt.retrieve.get`.
    strike : numeric
        Strike price.
    expiry : date or date str (e.g. '2015-01-01')
        Expiration date.

    Returns
    ------------
    metrics : DataFrame
        Metrics for evaluating straddle.
    """
    _callprice, _underlying, _qt = price.get(optdata, 'call', strike, expiry, False)
    _putprice = price.get(optdata, 'put', strike, expiry, False)[0]
    _index = ['Call', 'Put', 'Credit', 'Underlying', 'Quote_Time']
    _vals = np.array([_callprice, _putprice, _callprice + _putprice, _underlying, _qt])
    return pd.DataFrame(_vals, index=_index, columns=['Value'])
