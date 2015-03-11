"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - options class (:mod:`pynance.opt.core`)
=========================================================

.. currentmodule:: pynance.opt.core
"""

from __future__ import absolute_import

from .price import Price
from .spread.core import Spread

class Options(object):
    """
    Options data along with methods for easy access to desired information.

    .. versionadded:: 0.3.0

    Objects of this class are not intended for direct instantiation
    but are created by calling :func:`~pynance.opt.retrieve.get` 

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Dataframe containing the options data.

    Attributes
    ----------
    data : :class:`pandas.DataFrame`
        Options data.
    price : :class:`~pynance.opt.price.Price`
        Wrapper containing methods for determining price.
    spread : :class:`~pynance.opt.spread.core.Spread`
        Wrapper containing methods for evaluating spreads.

    Methods
    -------
    .. automethod:: exps

    .. automethod:: info

    .. automethod:: quotetime

    Examples
    --------
    Just retrieve data (no info message)::

    >>> geopt = pn.opt.get('ge')

    or retrieve data with info::
    
        >>> fopt, fexp = pn.opt.get('f').info()
        Expirations:
        ...
        Stock: 16.25
        Quote time: 2015-03-01 16:00
    """

    def __init__(self, df):
        self.data = df
        self.price = Price(df)
        self.spread = Spread(df)

    def info(self):
        """
        Show expiration dates, equity price, quote time.

        Returns
        -------
        self : :class:`~pynance.opt.core.Options`
            Returns a reference to the calling object to allow
            chaining.

        expiries : :class:`pandas.tseries.index.DatetimeIndex`

        Examples
        --------
        >>> fopt, fexp = pn.opt.get('f').info()
        Expirations:
        ...
        Stock: 16.25
        Quote time: 2015-03-01 16:00
        """
        print("Expirations:")
        _i = 0
        for _datetime in self.data.index.levels[1].to_pydatetime():
            print("{:2d} {}".format(_i, _datetime.strftime('%Y-%m-%d')))
            _i += 1
        print("Stock: {:.2f}".format(self.data.iloc[0].loc['Underlying_Price']))
        print("Quote time: {}".format(self.quotetime().strftime('%Y-%m-%d %H:%M%z')))
        return self, self.exps()

    def exps(self):
        """
        Index containing all expiration dates.

        Returns
        -------------
        expdates : :class:`pandas.tseries.index.DatetimeIndex`
            Index of all active expiration dates.
        """
        return self.data.index.levels[1]

    def quotetime(self):
        """
        Time of quotes

        Returns
        -------
        qt : :class:`datetime.datetime`
        """
        return self.data.iloc[0].loc['Quote_Time'].to_datetime()
