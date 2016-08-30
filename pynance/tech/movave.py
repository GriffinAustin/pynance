"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Technical analysis - moving averages (:mod:`pynance.tech.movave`)
==================================================================

.. currentmodule:: pynance.tech.movave
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from . import simple

def sma(eqdata, **kwargs):
    """ 
    simple moving average 

    Parameters
    ----------
    eqdata : DataFrame
    window : int, optional
        Lookback period for sma. Defaults to 20.
    outputcol : str, optional
        Column to use for output. Defaults to 'SMA'.
    selection : str, optional
        Column of eqdata on which to calculate sma. If
        `eqdata` has only 1 column, `selection` is ignored,
        and sma is calculated on that column. Defaults
        to 'Adj Close'.
    """
    if len(eqdata.shape) > 1 and eqdata.shape[1] != 1:
        _selection = kwargs.get('selection', 'Adj Close')
        _eqdata = eqdata.loc[:, _selection]
    else:
        _eqdata = eqdata
    _window = kwargs.get('window', 20)
    _outputcol = kwargs.get('outputcol', 'SMA')
    ret = pd.DataFrame(index=_eqdata.index, columns=[_outputcol], dtype=np.float64)
    ret.loc[:, _outputcol] = _eqdata.rolling(window=_window, center=False).mean().values.flatten()
    return ret

def ema(eqdata, **kwargs):
    """
    Exponential moving average with the given span.

    Parameters
    ----------
    eqdata : DataFrame
        Must have exactly 1 column on which to calculate EMA
    span : int, optional
        Span for exponential moving average. Cf. `pandas.stats.moments.ewma 
        <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.stats.moments.ewma.html>`_ and
        `additional Pandas documentation 
        <http://pandas.pydata.org/pandas-docs/stable/computation.html#exponentially-weighted-moment-functions>`_.
    outputcol : str, optional
        Column to use for output. Defaults to 'EMA'.
    selection : str, optional
        Column of eqdata on which to calculate ema. If
        `eqdata` has only 1 column, `selection` is ignored,
        and ema is calculated on that column. Defaults
        to 'Adj Close'.

    Returns
    ---------
    emadf : DataFrame
        Exponential moving average using the given `span`.
    """
    if len(eqdata.shape) > 1 and eqdata.shape[1] != 1:
        _selection = kwargs.get('selection', 'Adj Close')
        _eqdata = eqdata.loc[:, _selection]
    else:
        _eqdata = eqdata
    _span = kwargs.get('span', 20)
    _col = kwargs.get('outputcol', 'EMA')
    _emadf = pd.DataFrame(index=_eqdata.index, columns=[_col], dtype=np.float64)
    _emadf.loc[:, _col] = _eqdata.ewm(span=_span, min_periods=0, adjust=True, ignore_na=False).mean().values.flatten()
    return _emadf

def ema_growth(eqdata, **kwargs):
    """
    Growth of exponential moving average.

    Parameters
    ----------
    eqdata : DataFrame
    span : int, optional
        Span for exponential moving average. Defaults to 20.
    outputcol : str, optional.
        Column to use for output. Defaults to 'EMA Growth'.
    selection : str, optional
        Column of eqdata on which to calculate ema growth. If
        `eqdata` has only 1 column, `selection` is ignored,
        and ema growth is calculated on that column. Defaults
        to 'Adj Close'.

    Returns
    ---------
    out : DataFrame
        Growth of exponential moving average from one day to next
    """
    _growth_outputcol = kwargs.get('outputcol', 'EMA Growth')
    _ema_outputcol = 'EMA'
    kwargs['outputcol'] = _ema_outputcol
    _emadf = ema(eqdata, **kwargs)
    return simple.growth(_emadf, selection=_ema_outputcol, outputcol=_growth_outputcol)

def volatility(eqdata, **kwargs):
    """
    Volatility (standard deviation) over the given window

    Parameters
    ----------
    eqdata : DataFrame
    window : int, optional
        Lookback period. Defaults to 20.
    outputcol : str, optional
        Name of column to be used in returned dataframe. Defaults to 'Risk'.
    selection : str, optional
        Column of eqdata on which to calculate volatility. If
        `eqdata` has only 1 column, `selection` is ignored,
        and volatility is calculated on that column. Defaults
        to 'Adj Close'.

    Returns
    ---------
    risk : DataFrame
        Moving volatility with the given lookback.
    """
    if len(eqdata.shape) > 1 and eqdata.shape[1] != 1:
        _selection = kwargs.get('selection', 'Adj Close')
        _eqdata = eqdata.loc[:, _selection]
    else:
        _eqdata = eqdata
    _window = kwargs.get('window', 20)
    _colname = kwargs.get('outputcol', 'Risk')
    _risk = pd.DataFrame(index=_eqdata.index, columns=[_colname], dtype=np.float64)
    _risk.loc[:, _colname] = _eqdata.rolling(center=False, window=_window).std().values.flatten()
    return _risk

def growth_volatility(eqdata, **kwargs):
    """
    Return the volatility of growth.

    Note that, like :func:`pynance.tech.simple.growth` but in contrast to 
    :func:`volatility`, :func:`growth_volatility`
    applies directly to a dataframe like that returned by 
    :func:`pynance.data.retrieve.get`, not necessarily to a single-column dataframe.

    Parameters
    ----------
    eqdata : DataFrame
        Data from which to extract growth volatility. An exception
        will be raised if `eqdata` does not contain a column 'Adj Close'
        or an optional name specified by the `selection` parameter.
    window : int, optional
        Window on which to calculate volatility. Defaults to 20.
    selection : str, optional
        Column of eqdata on which to calculate volatility of growth. Defaults
        to 'Adj Close'
    outputcol : str, optional
        Column to use for output. Defaults to 'Growth Risk'.

    Returns
    ---------
    out : DataFrame
        Dataframe showing the volatility of growth over the specified `window`.
    """
    _window = kwargs.get('window', 20)
    _selection = kwargs.get('selection', 'Adj Close')
    _outputcol = kwargs.get('outputcol', 'Growth Risk')
    _growthdata = simple.growth(eqdata, selection=_selection)
    return volatility(_growthdata, outputcol=_outputcol, window=_window)

def bollinger(eqdata, **kwargs):
    """ 
    Bollinger bands

    Returns bolldf, smadf where bolldf is a DataFrame containing
    Bollinger bands with columns 'Upper' and 'Lower' and smadf contains
    the simple moving average.

    Parameters
    ----------
    eqdata : DataFrame
        Must include a column specified in the `selection` parameter or, 
        if no `selection` parameter is given, a column 'Adj Close'.
    window : int, optional
        Lookback period.
    multiple : float, optional
        Multiple of standard deviation above and below sma to use
        in calculating band value. Defaults to 2.0.
    selection : str, optional
        Column of `eqdata` on which to calculate bollinger bands.
        Defaults to 'Adj Close'.

    Returns
    ---------
    bolldf : DataFrame
        Dataframe containing columns 'Upper' and 'Lower' describing
        the given multiple of standard deviations above and below
        simple moving average for the lookback period.
    smadf : DataFrame
        Simple moving average given the specified lookback.
    """
    _window = kwargs.get('window', 20)
    _multiple = kwargs.get('multiple', 2.)
    _selection = kwargs.get('selection', 'Adj Close')
    # ensures correct name for output column of sma()
    kwargs['outputcol'] = 'SMA'
    _smadf = sma(eqdata, **kwargs)
    _sigmas = eqdata.loc[:, _selection].rolling(center=False, window=_window).std().values.flatten()
    _diff = _multiple * _sigmas
    _bolldf = pd.DataFrame(index=eqdata.index, columns=['Upper', 'Lower'], dtype=np.float64)
    _bolldf.loc[:, 'Upper'] = _smadf.iloc[:, 0].values + _diff
    _bolldf.loc[:, 'Lower'] = _smadf.iloc[:, 0].values - _diff
    return _bolldf, _smadf

def ratio_to_ave(window, eqdata, **kwargs):
    """
    Return values expressed as ratios to the average over some number
    of prior sessions.

    Parameters
    ----------
    eqdata : DataFrame
        Must contain a column with name matching `selection`, or, if
        `selection` is not specified, a column named 'Volume'
    window : int
        Interval over which to calculate the average. Normally 252 (1 year)
    selection : str, optional
        Column to select for calculating ratio. Defaults to 'Volume'
    skipstartrows : int, optional
        Rows to skip at beginning in addition to the `window` rows
        that must be skipped to get the baseline volume. Defaults to 0.
    skipendrows : int, optional
        Rows to skip at end. Defaults to 0.
    outputcol : str, optional
        Name of column in output dataframe. Defaults to 'Ratio to Ave'

    Returns
    ---------
    out : DataFrame
    """
    _selection = kwargs.get('selection', 'Volume')
    _skipstartrows = kwargs.get('skipstartrows', 0)
    _skipendrows = kwargs.get('skipendrows', 0)
    _outputcol = kwargs.get('outputcol', 'Ratio to Ave')
    _size = len(eqdata.index)
    _eqdata = eqdata.loc[:, _selection]

    _sma = _eqdata.iloc[:-1 - _skipendrows].rolling(window=window, center=False).mean().values
    _outdata = _eqdata.values[window + _skipstartrows:_size - _skipendrows] /\
            _sma[window + _skipstartrows - 1:]
    _index = eqdata.index[window + _skipstartrows:_size - _skipendrows]
    return pd.DataFrame(_outdata, index=_index, columns=[_outputcol], dtype=np.float64)
