PyNance chart example code: `bollinger.py`
==========================================

.. image:: /images/bollinger.png
    :align: center

::

    # candlestick chart showing simple moving average and 
    # Bollinger bands
    import pynance as pn

    def run():
        eqdata = pn.data.get('TSLA', '2015', '2016')
        bolldata, smadata = pn.tech.movave.bollinger(eqdata, selection='Close')
        pn.chart.candlestick(eqdata, title='TSLA 2015', bollinger=bolldata, sma=smadata)

    if __name__ == '__main__':
        run()
