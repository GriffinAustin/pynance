"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-07
@summary: Chart financial data

Since detailed charts are readily available online, these charts
serve 2 purposes:
1. Verify data integrity
2. Visualize events as defined by custom algorithms.
The functions in this submodule wrap pandas and matplotlib
for ease of use in serving these 2 purposes.

Resources:
http://matplotlib.org/api/finance_api.html
http://stackoverflow.com/questions/22027415/
http://sentdex.com/sentiment-analysisbig-data-and-python-tutorials-algorithmic-trading/how-to-chart-stocks-and-forex-doing-your-own-financial-charting/
http://stackoverflow.com/questions/19580116/plotting-candlestick-data-from-a-dataframe-in-python
http://sentdex.com/sentiment-analysisbig-data-and-python-tutorials-algorithmic-trading/how-to-chart-stocks-and-forex-doing-your-own-financial-charting/
http://pandas.pydata.org/pandas-docs/version/0.15.0/visualization.html
"""

import datetime as dt

import matplotlib.dates as mdates
import matplotlib.finance as fplt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def candlestick(df, **kwargs):
    """
    candlestick(df, title='GE', fname='foo.png', events=evdf, eventcolors=['r', 'g'], 
            bollinger=bolldf, sma=smadf)

    Show and optionally save candlestick chart of a DataFrame as retrieved using data.get().

    Parameters
    ---
    df : DataFrame containing columns 'Open', 'High', 'Low', 'Close' and 'Volume'
        source data
    title : str, optional
        title to be used for the chart
    fname : str, optional
        If provided, the chart will be saved to a file named `fname`. `fname`
        should also include the extension '.png' or '.pdf'
    events : DataFrame, optional (not implemented)
        must have the same index as df. 
        Non-events in this DataFrame should have a value like np.NAN,
        which matplotlib will not plot
    eventcolors : list of str, optional (not implemented)
        http://matplotlib.org/api/colors_api.html
    bollinger : DataFrame, optional (not implemented)
        if present Bollinger bands will be overlaid
        must have same index as df
        must contain columns 'Upper' and 'Lower'
    sma : DataFrame, optional (not implemented)
        if present, first data column will be overlaid as simple moving average
        must have same index as df
    """
    _make_chart(df, 'candlestick', **kwargs)

def adj_close(df, **kwargs):
    """
    adj_close(df, title='GE', fname='foo.png', events=evdf, eventcolors=['r', 'g'], 
            bollinger=bolldf, sma=smadf)

    Show and optionally save adj_close chart of a DataFrame as retrieved using data.get().

    Parameters
    ---
    df : DataFrame containing columns 'Open', 'High', 'Low', 'Close' and 'Volume'
        source data
    title : str, optional
        title to be used for the chart
    fname : str, optional
        If provided, the chart will be saved to a file named `fname`. `fname`
        should also include the extension '.png' or '.pdf'
    events : DataFrame, optional (not implemented)
        must have the same index as df. 
        Non-events in this DataFrame should have a value like np.NAN,
        which matplotlib will not plot
    eventcolors : list of str, optional (not implemented)
        http://matplotlib.org/api/colors_api.html
    bollinger : DataFrame, optional (not implemented)
        if present Bollinger bands will be overlaid
        must have same index as df
        must contain columns 'Upper' and 'Lower'
    sma : DataFrame, optional (not implemented)
        if present, first data column will be overlaid as simple moving average
        must have same index as df
    """
    _make_chart(df, 'adj_close', **kwargs)

def _make_chart(df, chart_type, **kwargs):
    fig = plt.figure()
    ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=4)
    ax1.grid(True)
    plt.ylabel('Price')
    plt.setp(plt.gca().get_xticklabels(), visible=False)
    if chart_type == 'candlestick':
        _candlestick_ax(df, ax1)
    elif chart_type == 'adj_close':
        _adj_close_ax(df, ax1)

    ax2 = plt.subplot2grid((5, 4), (4, 0), sharex=ax1, rowspan=1, colspan=4)
    ax2.bar(df.index, df.loc[:, 'Volume'])
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(12))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_minor_locator(mdates.DayLocator())
    ax2.yaxis.set_ticklabels([])
    ax2.grid(True)
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.subplots_adjust(left=.09, bottom=.18, right=.94, top=0.94, wspace=.20, hspace=0)
    if 'title' in kwargs:
        plt.suptitle(kwargs['title'])
    if 'fname' in kwargs:
        plt.savefig(kwargs['fname'], bbox_inches='tight')
    plt.show()
    plt.close()

def _candlestick_ax(df, ax):
    """
    # Alternatively: (but hard to get dates set up properly)
    plt.xticks(range(len(df.index)), df.index, rotation=45)
    fplt.candlestick2_ohlc(ax, df.loc[:, 'Open'].values, df.loc[:, 'High'].values, 
            df.loc[:, 'Low'].values, df.loc[:, 'Close'].values, width=0.2)
    """
    quotes = df.reset_index()
    quotes.loc[:, 'Date'] = mdates.date2num(quotes.loc[:, 'Date'].astype(dt.date))
    fplt.candlestick_ohlc(ax, quotes.values)

def _adj_close_ax(df, ax):
    ax.plot(df.index, df.loc[:, 'Adj Close'])
