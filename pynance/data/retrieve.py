"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Data - remote retrieval (:mod:`pynance.data.retrieve`)
=========================================================

.. currentmodule:: pynance.data.retrieve

Wraps `Pandas Remote Data Access 
<http://pandas.pydata.org/pandas-docs/stable/remote_data.html>`_.
"""

import pandas.io.data as web

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
