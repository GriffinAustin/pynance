"""
Functions for analysing options spreads.

Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from . import price

def calendar(optdata, opttype, strike, expiry1, expiry2):
    """
    Metrics for evaluating a simple calendar spread.

    Parameters
    --
    optdata : DataFrame
        Data returned from `pn.opt.get()`

    opttype : str {'call', 'put'}
        Type of option on which to collect data.

    strike : numeric
        Strike price.

    expiry1 : date or date str (e.g. '2015-01-01')
        Earlier expiration date.

    expiry2 : date or date str (e.g. '2015-01-01')
        Later expiration date.

    Returns
    --
    metrics : DataFrame
        Metrics for evaluating spread.
    """
    _price1, _underlying = price.get(optdata, opttype, strike, expiry1, False)
    _price2, _ = price.get(optdata, opttype, strike, expiry2, False)
    _index = ['Near', 'Far', 'Debit', 'Underlying']
    _vals = np.array([_price1, _price2, _price2 - _price1, _underlying])
    return pd.DataFrame(_vals, index=_index, columns=['Value'])

def dbl_calendar(opdata, putstrike, callstrike, expiry1, expiry2):
    pass

def straddle(optdata, strike, expiry):
    """
    Metrics for evaluating a straddle

    Parameters
    --
    optdata : DataFrame
        Data returned from `pn.opt.get()`.

    strike : numeric
        Strike price.

    expiry : date or date str (e.g. '2015-01-01')
        Expiration date.

    Returns
    --
    metrics : DataFrame
        Metrics for evaluating straddle.
    """
    _callprice, _underlying = price.get(optdata, 'call', strike, expiry, False)
    _putprice, _ = price.get(optdata, 'put', strike, expiry, False)
    _index = ['Call', 'Put', 'Credit', 'Underlying']
    _vals = np.array([_callprice, _putprice, _callprice + _putprice, _underlying])
    return pd.DataFrame(_vals, index=_index, columns=['Value'])
