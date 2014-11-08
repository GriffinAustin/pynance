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
http://stackoverflow.com/questions/19580116/plotting-candlestick-data-from-a-dataframe-in-python
http://sentdex.com/sentiment-analysisbig-data-and-python-tutorials-algorithmic-trading/how-to-chart-stocks-and-forex-doing-your-own-financial-charting/
http://pandas.pydata.org/pandas-docs/version/0.15.0/visualization.html
"""

import datetime as dt

import matplotlib.dates as mdates
import matplotlib.finance as fplt
import matplotlib.pyplot as plt

def candlestick(df, **kwargs):
    #TODO include volume in chart
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
        must have the same index as df. Entries in this DataFrame will be evaluated
        as booleans where `True` represents an event and `False` a non-event. Events
        markers will be overlaid on the chart.
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
    fig, ax = plt.subplots()
    # works, but leaves gaps for days when market is closed
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    fig.subplots_adjust(bottom=0.2)
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.grid()
    quotes = df.reset_index()
    quotes.loc[:, 'Date'] = mdates.date2num(quotes.loc[:, 'Date'].astype(dt.date))
    fplt.candlestick_ohlc(ax, quotes.values)
    """
    # Alternatively: (but hard to get dates set up properly)
    plt.xticks(range(len(df.index)), df.index, rotation=45)
    fplt.candlestick2_ohlc(ax, df.loc[:, 'Open'].values, df.loc[:, 'High'].values, 
            df.loc[:, 'Low'].values, df.loc[:, 'Close'].values, width=0.2)
    """
    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
    if 'fname' in kwargs:
        plt.savefig(kwargs['fname'], bbox_inches='tight')
    plt.show()
    plt.close()

def adj_close(df, **kwargs):
    # TODO
    pass
