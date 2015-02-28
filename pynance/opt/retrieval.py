"""
Functions for retrieving options data.

Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

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
    return _optmeta.get_all_data()
