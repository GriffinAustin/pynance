"""
Functions for extracting price and time-value.

Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import pandas as pd

def get(optdata, opttype, strike, expiry, showtimeval=True):
    """
    Retrieve price and time value of an option.

    Parameters
    --
    optdata : DataFrame
        Data returned from `pn.opt.get()`

    opttype : str {'call', 'put'}
        Type of option on which to collect data.

    strike : numeric
        Strike price.

    expiry : date or date str (e.g. '2015-01-01')
        Expiration date.

    showtimeval : bool, optional
        Whether or not to include time value calculation. Setting
        this value to false will save time if the function is potentially
        being used inside a loop. Defaults to True.

    Returns
    --
    opt_price : float
        Price of option (midpoint between bid and ask).

    underlying_price : float
        Price of underlying.

    time_value : float
        Time value of option. Returned only as long as `showtimeval` is set
        to True.
    """
    _optrow = optdata.loc[(strike, expiry, opttype), :]
    _opt_price = _getprice(_optrow)
    _underlying_price = _optrow.loc[:, 'Underlying_Price'].values[0]
    if showtimeval:
        if opttype == 'put':
            _timevalue = _get_put_time_val(_opt_price, strike, _underlying_price)
        else:
            _timevalue = _get_call_time_val(_opt_price, strike, _underlying_price)
        return _opt_price, _underlying_price, _timevalue
    return _opt_price, _underlying_price

def allstrikes(optdata, opttype, expiry):
    """
    Retrieve option prices for all strikes of a given type with a given expiration.

    Parameters
    --
    optdata : DataFrame

    opttype : str {'call', 'put'}

    expiry : date or date str

    Returns
    --
    df : DataFrame

    underlying : float
        Price of underlying.

    quote_time : pandas.tslib.Timestamp
        Time of quote.
    """
    _relevant = optdata.loc[(slice(None), expiry, opttype), :]
    _index = _relevant.index.get_level_values('Strike')
    _columns = ['Price', 'Time_Val', 'Last', 'Bid', 'Ask', 'Vol', 'Open_Int']
    _df = pd.DataFrame(index=_index, columns=_columns)
    _underlying = _relevant.loc[:, 'Underlying_Price'].values[0]
    _quotetime = pd.to_datetime(_relevant.loc[:, 'Quote_Time'].values[0])
    for _col in _columns[2:]:
        _df.loc[:, _col] = _relevant.loc[:, _col].values
    _df.loc[:, 'Price'] = (_df.loc[:, 'Bid'] + _df.loc[:, 'Ask']) / 2.
    _set_tv_strike_ix(_df, opttype, 'Price', 'Time_Val', _underlying)
    return _df, _underlying, _quotetime

def allexpiries(optdata, opttype, strike):
    """
    Prices for given strike on all available dates.

    Parameters
    --
    optdata : DataFrame

    opttype : str {'call', 'put'}

    strike : numeric

    Returns
    --
    df : DataFrame

    underlying : float
        Price of underlying.

    quote_time : pandas.tslib.Timestamp
        Time of quote.
    """
    _relevant = optdata.loc[(strike, slice(None), opttype), :]
    _index = _relevant.index.get_level_values('Expiry')
    _columns = ['Price', 'Time_Val', 'Last', 'Bid', 'Ask', 'Vol', 'Open_Int']
    _df = pd.DataFrame(index=_index, columns=_columns)
    _underlying = _relevant.loc[:, 'Underlying_Price'].values[0]
    _quotetime = pd.to_datetime(_relevant.loc[:, 'Quote_Time'].values[0])
    for _col in _columns[2:]:
        _df.loc[:, _col] = _relevant.loc[:, _col].values
    _df.loc[:, 'Price'] = (_df.loc[:, 'Bid'] + _df.loc[:, 'Ask']) / 2.
    _set_tv_other_ix(_df, opttype, 'Price', 'Time_Val', _underlying, strike)
    return _df, _underlying, _quotetime

def _set_tv_other_ix(df, opttype, pricecol, tvcol, eqprice, strike):
    if opttype == 'put':
        if strike <= eqprice:
            df.loc[:, tvcol] = df.loc[:, pricecol]
        else:
            _diff = eqprice - strike
            df.loc[:, tvcol] = df.loc[:, pricecol] + _diff
    else:
        if eqprice <= strike:
            df.loc[:, tvcol] = df.loc[:, pricecol]
        else:
            _diff = strike - eqprice
            df.loc[:, tvcol] = df.loc[:, pricecol] + _diff

def _set_tv_strike_ix(df, opttype, pricecol, tvcol, eqprice):
    df.loc[:, tvcol] = df.loc[:, pricecol]
    if opttype == 'put':
        _mask = (df.index > eqprice)
        df.loc[_mask, tvcol] += eqprice - df.index[_mask]
    else:
        _mask = (df.index < eqprice)
        df.loc[_mask, tvcol] += df.index[_mask] - eqprice
    return

def _getprice(optrow):
    _bid = optrow.loc[:, 'Bid'].values[0]
    _ask = optrow.loc[:, 'Ask'].values[0]
    return (_bid + _ask) / 2.

def _get_put_time_val(putprice, strike, eqprice):
    if strike <= eqprice:
        return putprice
    return putprice + eqprice - strike
    
def _get_call_time_val(callprice, strike, eqprice):
    if eqprice <= strike:
        return callprice
    return callprice + strike - eqprice
