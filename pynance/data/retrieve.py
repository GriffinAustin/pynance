"""
Data retrieval

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

Wraps Pandas Remote Data Access: 
http://pandas.pydata.org/pandas-docs/stable/remote_data.html
"""

import pandas.io.data as web

def get(equity, start, end):
    """ Get DataFrame for an individual equity from Yahoo!  """
    return web.DataReader(equity, 'yahoo', start, end)
