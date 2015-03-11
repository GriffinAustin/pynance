"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - diagonal spreads (:mod:`pynance.opt.spread.diag`)
=============================================================

.. currentmodule:: pynance.opt.spread.diag
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from .._common import _getkeys
from .._common import _getprice
from .._common import _relevant_rows
from .. import _constants


class Diag(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on horizontal (calendar) spreads

    Objects of this class are not intended for direct instantiation
    but are created as attributes of objects of type 
    :class:`~pynance.opt.spread.core.Spread`.

    .. versionadded:: 0.3.0

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data : :class:`pandas.DataFrame`

    Methods
    -------
    .. automethod:: dblcal

    .. automethod:: diagbtrfly
    """
    def __init__(self, df):
        self.data = df

    def dblcal(self, lowstrike, highstrike, expiry1, expiry2):
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
        _rows1 = {}
        _rows2 = {}
        _prices1 = {}
        _prices2 = {}
        _index = ['Near Call', 'Far Call', 'Call Ratio', 'Near Put', 'Far Put', 
                'Put Ratio', 'Near to Far Ratio', 'Debit', 'Underlying_Price', 'Quote_Time']
        _metrics = pd.DataFrame(index=_index, columns=['Value'])
        _errmsg = "No key for {} strike {} {}"
        _opttype = 'call'
        _rows1[_opttype] = _relevant_rows(self.data, (highstrike, expiry1, _opttype),
                _errmsg.format(expiry1, highstrike, _opttype))
        _prices1[_opttype] = _getprice(_rows1[_opttype])
        _rows2[_opttype] = _relevant_rows(self.data, (highstrike, expiry2, _opttype),
                _errmsg.format(expiry2, highstrike, _opttype))
        _prices2[_opttype] = _getprice(_rows2[_opttype])
        _metrics.loc['Near Call', 'Value'] = _prices1[_opttype]
        _metrics.loc['Far Call', 'Value'] = _prices2[_opttype]
        _metrics.loc['Call Ratio', 'Value'] = _prices1[_opttype] / _prices2[_opttype]
        _metrics.loc['Underlying_Price', 'Value'], _metrics.loc['Quote_Time', 'Value'] =\
                _getkeys(_rows1[_opttype], ['Underlying_Price', 'Quote_Time'])
        _opttype = 'put'
        _rows1[_opttype] = _relevant_rows(self.data, (lowstrike, expiry1, _opttype),
                _errmsg.format(expiry1, lowstrike, _opttype))
        _prices1[_opttype] = _getprice(_rows1[_opttype])
        _rows2[_opttype] = _relevant_rows(self.data, (lowstrike, expiry2, _opttype),
                _errmsg.format(expiry2, lowstrike, _opttype))
        _prices2[_opttype] = _getprice(_rows2[_opttype])
        _metrics.loc['Near Put', 'Value'] = _prices1[_opttype]
        _metrics.loc['Far Put', 'Value'] = _prices2[_opttype]
        _metrics.loc['Put Ratio', 'Value'] = _prices1[_opttype] / _prices2[_opttype]
        _neartot = sum(_prices1.values())
        _fartot = sum(_prices2.values())
        _metrics.loc['Near to Far Ratio', 'Value'] = float(_neartot) / _fartot
        _metrics.loc['Debit', 'Value'] = _fartot - _neartot
        return _metrics

    def diagbtrfly(self, lowstrike, midstrike, highstrike, expiry1, expiry2):
        """
        Metrics for evaluating a diagonal butterfly spread.

        Parameters
        ------------
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
        _rows1 = {}
        _rows2 = {}
        _prices1 = {}
        _prices2 = {}
        _index = ['Straddle Call', 'Straddle Put', 'Straddle Total', 'Far Call', 'Far Put', 'Far Total',
                'Straddle to Far Ratio', 'Credit', 'Underlying_Price', 'Quote_Time']
        _metrics = pd.DataFrame(index=_index, columns=['Value'])
        _errmsg = "No key for {} strike {} {}"
        _opttype = 'call'
        _rows1[_opttype] = _relevant_rows(self.data, (midstrike, expiry1, _opttype),
                _errmsg.format(expiry1, midstrike, _opttype))
        _prices1[_opttype] = _getprice(_rows1[_opttype])
        _rows2[_opttype] = _relevant_rows(self.data, (highstrike, expiry2, _opttype),
                _errmsg.format(expiry2, highstrike, _opttype))
        _prices2[_opttype] = _getprice(_rows2[_opttype])
        _metrics.loc['Straddle Call', 'Value'] = _prices1[_opttype]
        _metrics.loc['Far Call', 'Value'] = _prices2[_opttype]
        _metrics.loc['Underlying_Price', 'Value'], _metrics.loc['Quote_Time', 'Value'] =\
                _getkeys(_rows1[_opttype], ['Underlying_Price', 'Quote_Time'])
        _opttype = 'put'
        _rows1[_opttype] = _relevant_rows(self.data, (midstrike, expiry1, _opttype),
                _errmsg.format(expiry1, midstrike, _opttype))
        _prices1[_opttype] = _getprice(_rows1[_opttype])
        _rows2[_opttype] = _relevant_rows(self.data, (lowstrike, expiry2, _opttype),
                _errmsg.format(expiry2, lowstrike, _opttype))
        _prices2[_opttype] = _getprice(_rows2[_opttype])
        _metrics.loc['Straddle Put', 'Value'] = _prices1[_opttype]
        _metrics.loc['Far Put', 'Value'] = _prices2[_opttype]
        _metrics.loc['Straddle Total', 'Value'] = _neartot = sum(_prices1.values())
        _metrics.loc['Far Total', 'Value'] = _fartot = sum(_prices2.values())
        _metrics.loc['Straddle to Far Ratio', 'Value'] = _neartot / _fartot 
        _metrics.loc['Credit', 'Value'] = _neartot - _fartot
        return _metrics
