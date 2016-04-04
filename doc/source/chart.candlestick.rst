PyNance chart example code: `candlestick.py`
============================================

.. image:: /images/candlestick.png
    :align: center

::

    # basic candlestick chart
    import pynance as pn

    def run():
        df = pn.data.get('TSLA', '2015', '2016')
        pn.chart.candlestick(df, title='TSLA 2015')

    if __name__ == '__main__':
        run()
