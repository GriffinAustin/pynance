"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - remote retrieval (:mod:`pynance.data.retrieve`)
=========================================================

.. currentmodule:: pynance.data.retrieve

Wraps `Pandas Remote Data Access 
<http://pandas.pydata.org/pandas-docs/stable/remote_data.html>`_.
"""
import os
from ftplib import FTP
from functools import partial
import io

import pandas as pd
import pandas_datareader.data as web

import pynance as pn

def get(equity, *args, **kwargs):
    """get(equity, start=None, end=None)
    Get DataFrame for an individual equity from Yahoo!  

    .. versionchanged:: 0.5.0
       Default `start` (2001-01-31) and `end` (current date).
    
    Examples
    --------
    >>> import pynance as pn
    >>> aapl = pn.data.get('aapl', '2014-03-01', '2015-03-01')
    >>> goog = pn.data.get('goog', '2014')
    """
    df = web.DataReader(equity, 'stooq', *args, **kwargs)
    df.index = pd.to_datetime(df.index)
    return df


def equities(country='US'):
    """
    Return a DataFrame of current US equities.

    .. versionadded:: 0.4.0

    .. versionchanged:: 0.5.0
       Return a DataFrame

    Parameters
    ----------
    country : str, optional
        Country code for equities to return, defaults to 'US'.

    Returns
    -------
    eqs : :class:`pandas.DataFrame`
        DataFrame whose index is a list of all current ticker symbols.
        Columns are 'Security Name' (e.g. 'Zynerba Pharmaceuticals, Inc. - Common Stock')
        and 'Exchange' ('NASDAQ', 'NYSE', 'NYSE MKT', etc.)

    Examples
    --------
    >>> eqs = pn.data.equities('US')

    Notes
    -----
    Currently only US markets are supported.
    """
    nasdaqblob, otherblob = _getrawdata()
    eq_triples = []
    eq_triples.extend(_get_nas_triples(nasdaqblob))
    eq_triples.extend(_get_other_triples(otherblob))
    eq_triples.sort()
    index = [triple[0] for triple in eq_triples]
    data = [triple[1:] for triple in eq_triples]
    return pd.DataFrame(data, index, columns=['Security Name', 'Exchange'], dtype=str)

def _get_nas_triples(blob):
    return _get_triples(blob, {}, 'NASDAQ')

def _get_other_triples(blob):
    # http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
    exchanges = {
            'A': 'NYSE MKT',
            'N': 'NYSE',
            'P': 'NYSE ARCA',
            'Z': 'BATS'}
    return _get_triples(blob, exchanges, 'unknown')

def _get_triples(blob, exchanges, default):
    lines = blob.splitlines()
    fields = [line.split('|') for line in lines[1:]] 
    # last line is generally file info
    if not fields[-1][1].isalpha() or not fields[-1][2].isalpha():
        return [(field[0], field[1], exchanges.get(field[2], default)) for field in fields[:-1]]
    return [(field[0], field[1], exchanges.get(field[2], default)) for field in fields]

def _getrawdata():
    # http://quant.stackexchange.com/questions/1640/where-to-download-list-of-all-common-stocks-traded-on-nyse-nasdaq-and-amex
    _nasdaqio = io.BytesIO()
    _otherio = io.BytesIO()
    _host = 'ftp.nasdaqtrader.com'
    _directory = 'symboldirectory'
    _nasdaqfile = 'nasdaqlisted.txt'
    _otherfile = 'otherlisted.txt'
    _ftp = FTP(_host)
    _ftp.login()
    _ftp.cwd(_directory)
    _ftp.retrbinary('RETR ' + _nasdaqfile, partial(_handle_binary, _nasdaqio))
    _ftp.retrbinary('RETR ' + _otherfile, partial(_handle_binary, _otherio))
    _ftp.quit()
    _nasdaq = _nasdaqio.getvalue()
    _nasdaqio.close()
    _other = _otherio.getvalue()
    _otherio.close()
    return _nasdaq.decode("utf-8"), _other.decode("utf-8")

def _handle_binary(sio, more_data):
    # http://stackoverflow.com/questions/18772703/read-a-file-in-buffer-from-ftp-python
    sio.write(more_data)
