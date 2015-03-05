"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - remote retrieval (:mod:`pynance.opt.retrieve`)
=========================================================

.. currentmodule:: pynance.opt.retrieve
"""

from __future__ import absolute_import

import pandas
from pandas.io.data import Options

from . import constants

def get(equity, showinfo=True):
    """
    Retrieve all current options chains for given equity.

    Parameters
    -------------
    equity : str
        Equity for which to retrieve options data.

    showinfo : bool, optional
        If true (default), available expiries and equity price are 
        printed to console. 

    Returns
    -------------
    optdata : DataFrame
        All options data for given equity currently available
        from Yahoo! Finance.

    expdates : pandas.tseries.index.DatetimeIndex
        Index of all active expiration dates.

    eqprice : float
        Price of underlying equity at the time options data
        was retrieved.
        
    Notes
    -------------
    For convenience, expiration dates are shown by default. So you
    don't have to call other functions to figure out what the exact expiration
    dates are for the various options you might be considering.
    An index of the expiration timestamps is also returned,
    so that you can then pass dates not only in the form
    '2015-08-21' (or other object are formats that pandas
    can convert to timestamps) but also as a numerical index
    in pandas timeseries (cf. example below).

    To disable this feature and return a single dataframe of options
    data, set the `showinfo` argument to False.

    Examples
    -------------
    >>> fopt, fexp, feq = pn.opt.get('f')
    Expirations:
    ...
    >>> fstraddle = pn.opt.spread.straddle(fopt, 16, fexp[4])
    """
    _optmeta = Options(equity, 'yahoo')
    _optdata = None
    try:
        _optdata = _optmeta.get_all_data()
    except (AttributeError, ValueError, pandas.io.data.RemoteDataError):
        raise pandas.io.data.RemoteDataError(
                "No options data available for {!r}".format(equity))
    if showinfo:
        print("Expirations:")
        showexpiries(_optdata)
        print("Stock: {:.2f}".format(_optdata.iloc[0].loc['Underlying_Price']))
    return _optdata, _optdata.index.levels[1], round(_optdata.iloc[0].loc['Underlying_Price'],
            constants.NDIGITS_SIG)

def getexpiries(optdata):
    """
    Get all expiration dates contained in the data index.

    Parameters
    -------------
    optdata : DataFrame
        Collection of options data as retrieved from `pn.opt.get()`

    Returns
    -------------
    expdates : pandas.tseries.index.DatetimeIndex
        Index of all active expiration dates.
    """
    return optdata.index.levels[1]

def showexpiries(optdata):
    """
    Show all expiration dates but return nothing

    Parameters
    -------------
    optdata : DataFrame
        Collection of options data as retrieved from `pn.opt.get()`
    """
    _i = 0
    for _datetime in optdata.index.levels[1].to_pydatetime():
        print("{:2d} {}".format(_i, _datetime.strftime('%Y-%m-%d')))
        _i += 1
