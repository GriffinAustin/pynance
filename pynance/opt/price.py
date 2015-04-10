"""
.. Copyright (c) 2014, 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - price (:mod:`pynance.opt.price`)
==================================================

.. currentmodule:: pynance.opt.price
"""

from __future__ import absolute_import

import pandas as pd

from ._common import _getprice
from ._common import _relevant_rows
from . import _constants

class Price(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    options prices.

    Objects of this class are not intended for direct instantiation
    but are created as attributes of objects of type :class:`~pynance.opt.core.Options`.

    .. versionadded:: 0.3.0

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data : :class:`pandas.DataFrame`
        Options data.

    Methods
    -------
    .. automethod:: exps

    .. automethod:: get

    .. automethod:: metrics

    .. automethod:: strikes
    """
    def __init__(self, df):
        self.data = df

    def get(self, opttype, strike, expiry):
        """
        Price as midpoint between bid and ask.

        Parameters
        ----------
        opttype : str
            'call' or 'put'.
        strike : numeric
            Strike price.
        expiry : date-like
            Expiration date. Can be a :class:`datetime.datetime` or
            a string that :mod:`pandas` can interpret as such, e.g.
            '2015-01-01'.

        Returns
        -------
        out : float

        Examples
        --------
        >>> geopts = pn.opt.get('ge')
        >>> geopts.price.get('call', 26., '2015-09-18')
        0.94
        """
        _optrow = _relevant_rows(self.data, (strike, expiry, opttype,),
                "No key for {} strike {} {}".format(expiry, strike, opttype))
        return _getprice(_optrow)

    def metrics(self, opttype, strike, expiry):
        """
        Basic metrics for a specific option.

        Parameters
        ----------
        opttype : str ('call' or 'put')
        strike : numeric
            Strike price.
        expiry : date-like
            Expiration date. Can be a :class:`datetime.datetime` or
            a string that :mod:`pandas` can interpret as such, e.g.
            '2015-01-01'.

        Returns
        -------
        out : :class:`pandas.DataFrame`
        """
        _optrow = _relevant_rows(self.data, (strike, expiry, opttype,),
                "No key for {} strike {} {}".format(expiry, strike, opttype))
        _index = ['Opt_Price', 'Time_Val', 'Last', 'Bid', 'Ask', 'Vol', 'Open_Int', 'Underlying_Price', 'Quote_Time']
        _out = pd.DataFrame(index=_index, columns=['Value'])
        _out.loc['Opt_Price', 'Value'] = _opt_price = _getprice(_optrow)
        for _name in _index[2:]:
            _out.loc[_name, 'Value'] = _optrow.loc[:, _name].values[0]
        _eq_price = _out.loc['Underlying_Price', 'Value']
        if opttype == 'put':
            _out.loc['Time_Val'] = _get_put_time_val(_opt_price, strike, _eq_price)
        else:
            _out.loc['Time_Val'] = _get_call_time_val(_opt_price, strike, _eq_price)
        return _out

    def strikes(self, opttype, expiry):
        """
        Retrieve option prices for all strikes of a given type with a given expiration.

        Parameters
        ----------
        opttype : str ('call' or 'put')
        expiry : date-like
            Expiration date. Can be a :class:`datetime.datetime` or
            a string that :mod:`pandas` can interpret as such, e.g.
            '2015-01-01'.

        Returns
        ----------
        df : :class:`pandas.DataFrame`
        eq : float
            Price of underlying.
        qt : datetime.datetime
            Time of quote.

        See Also
        --------
        :meth:`exps`
        """
        _relevant = _relevant_rows(self.data, (slice(None), expiry, opttype,),
                "No key for {} {}".format(expiry, opttype))
        _index = _relevant.index.get_level_values('Strike')
        _columns = ['Price', 'Time_Val', 'Last', 'Bid', 'Ask', 'Vol', 'Open_Int']
        _df = pd.DataFrame(index=_index, columns=_columns)
        _underlying = _relevant.loc[:, 'Underlying_Price'].values[0]
        _quotetime = pd.to_datetime(_relevant.loc[:, 'Quote_Time'].values[0], utc=True).to_datetime()
        for _col in _columns[2:]:
            _df.loc[:, _col] = _relevant.loc[:, _col].values
        _df.loc[:, 'Price'] = (_df.loc[:, 'Bid'] + _df.loc[:, 'Ask']) / 2.
        _set_tv_strike_ix(_df, opttype, 'Price', 'Time_Val', _underlying)
        return _df, _underlying, _quotetime

    def exps(self, opttype, strike):
        """
        Prices for given strike on all available dates.

        Parameters
        ----------
        opttype : str ('call' or 'put')
        strike : numeric

        Returns
        ----------
        df : :class:`pandas.DataFrame`
        eq : float
            Price of underlying.
        qt : :class:`datetime.datetime`
            Time of quote.

        See Also
        --------
        :meth:`strikes`
        """
        _relevant = _relevant_rows(self.data, (strike, slice(None), opttype,),
                "No key for {} {}".format(strike, opttype))
        _index = _relevant.index.get_level_values('Expiry')
        _columns = ['Price', 'Time_Val', 'Last', 'Bid', 'Ask', 'Vol', 'Open_Int']
        _df = pd.DataFrame(index=_index, columns=_columns)
        _eq = _relevant.loc[:, 'Underlying_Price'].values[0]
        _qt = pd.to_datetime(_relevant.loc[:, 'Quote_Time'].values[0], utc=True).to_datetime()
        for _col in _columns[2:]:
            _df.loc[:, _col] = _relevant.loc[:, _col].values
        _df.loc[:, 'Price'] = (_df.loc[:, 'Bid'] + _df.loc[:, 'Ask']) / 2.
        _set_tv_other_ix(_df, opttype, 'Price', 'Time_Val', _eq, strike)
        return _df, _eq, _qt

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

def _get_put_time_val(putprice, strike, eqprice):
    if strike <= eqprice:
        return putprice
    return round(putprice + eqprice - strike, _constants.NDIGITS_SIG)
    
def _get_call_time_val(callprice, strike, eqprice):
    if eqprice <= strike:
        return callprice
    return round(callprice + strike - eqprice, _constants.NDIGITS_SIG)
