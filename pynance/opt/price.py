"""
Functions for extracting price and time-value.

Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

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
