"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - remote retrieval (:mod:`pynance.data.retrieve`)
=========================================================

.. currentmodule:: pynance.data.retrieve

Wraps `Pandas Remote Data Access 
<http://pandas.pydata.org/pandas-docs/stable/remote_data.html>`_.
"""

from ftplib import FTP
from functools import partial
import io

import pandas_datareader.data as web

def get(equity, start, end):
    """ 
    Get DataFrame for an individual equity from Yahoo!  
    
    Examples
    --------
    >>> import pynance as pn
    >>> aapl = pn.data.get('aapl', '2014-03-01', '2015-03-01')
    >>> goog = pn.data.get('goog', '2014', '2015')
    """
    return web.DataReader(equity, 'yahoo', start, end)

def equities(country='US'):
    """
    Return a dictionary of equities and the exchange where
    they are traded.

    Currently only US markets are supported

    .. versionadded:: 0.4.0

    Parameters
    ----------
    country : str, optional
        Country code for equities to return, defaults to 'US'.

    Returns
    -------
    eq : dict of str
        Dictionary mapping equities to a string representing the exchange
        on which they are traded.

    Examples
    --------
    >>> equities = pn.data.equities('US')
    """
    _nasdaqblob, _otherblob = _getrawdata()
    return _fromblobs(_nasdaqblob, _otherblob)

def _fromblobs(nasdaqblob, otherblob):
    _nasdaq = nasdaqblob.splitlines()
    _other = otherblob.splitlines()
    _nasdaqequities = [line.partition('|')[0] for line in _nasdaq[1:]]
    # last line may contain file info
    while not _nasdaqequities[-1].isalpha():
        _nasdaqequities.pop()
    _equities = {key: 'NASDAQ' for key in _nasdaqequities}
    _equities.update(_linestodict(_other[1:]))
    return _equities

def _linestodict(lines):
    _rows = [line.split('|', 3) for line in lines]
    # last line may contain file info
    while not _rows[-1][0].isalpha():
        _rows.pop()
    # http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
    _exchanges = {
            'A': 'NYSE MKT',
            'N': 'NYSE',
            'P': 'NYSE ARCA',
            'Z': 'BATS'
            }
    _equities = {_row[0]: _exchanges.get(_row[2], 'unknown') for _row in _rows}
    return _equities

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
