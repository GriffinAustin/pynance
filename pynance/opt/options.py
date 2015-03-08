"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - remote retrieval (:mod:`pynance.opt.options`)
=========================================================

.. currentmodule:: pynance.opt.options
"""

from __future__ import absolute_import

from .price import Price

class Options(object):
    """
    Options data along with methods for easy access to desired information.

    .. versionadded:: 0.3.0

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Dataframe containing the options data.

    Attributes
    ----------
    data

    Examples
    --------
    >>> import pynance as pn
    >>> fopt = pn.opt.get('f').info()
    Expirations:
    ...
    Stock: 16.25
    Quote time: 2015-03-01 16:00
    >>>
    """

    def __init__(self, df):
        self.data = df

    def info(self):
        """
        Show expiration dates, equity price, quote time.

        Returns
        -------
        self : :class:`pynance.opt.options.Options`
            Returns a reference to the calling object to allow
            chaining.
        """
        print("Expirations:")
        _i = 0
        for _datetime in self.data.index.levels[1].to_pydatetime():
            print("{:2d} {}".format(_i, _datetime.strftime('%Y-%m-%d')))
            _i += 1
        print("Stock: {:.2f}".format(self.data.iloc[0].loc['Underlying_Price']))
        print("Quote time: {}".format(self.quotetime().strftime('%Y-%m-%d %H:%M%z')))
        return self

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

    def price(self):
        """
        Return a wrapper providing easy access to price data.

        Returns
        -------
        out : :class:`pynance.opt.price.Price`
        """
        return Price(self.data)
