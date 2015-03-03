"""
Functions for retrieving options data.

Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import pandas
from pandas.io.data import Options

def get(equity):
    """
    Retrieve all current options chains for given equity.

    Parameters
    --
    equity : str
        Equity for which to retrieve options data.

    Returns
    --
    optdata : DataFrame
        All options data for given equity currently available
        from Yahoo! Finance.

    # optmeta : pandas.io.data.Options
    #    Object containing options metadata, such as a list
    #    of expiration dates.
    """
    _optmeta = Options(equity, 'yahoo')
    try:
        return _optmeta.get_all_data()
    except (AttributeError, ValueError, pandas.io.data.RemoteDataError):
        raise pandas.io.data.RemoteDataError(
                "No options data available for {!r}".format(equity))

def expiries(optdata):
    """
    Get all expiration dates contained in the data index.

    Parameters
    --
    optdata : DataFrame
        Collection of options data as retrieved from `pn.opt.get()`

    Returns
    --
    expdates : list {pandas.tslib.Timestamp}
        List of all active expiration dates.
    """
    return list(optdata.index.levels[1])

def showdates(optdata):
    """
    Show all expiration dates but return nothing

    Parameters
    --
    optdata : DataFrame
        Collection of options data as retrieved from `pn.opt.get()`
    """
    for _datetime in optdata.index.levels[1].to_pydatetime():
        print(_datetime.strftime('%Y-%m-%d'))
