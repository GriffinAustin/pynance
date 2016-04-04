PyNance chart example code: `sma.py`
====================================

.. image:: /images/sma.png
    :align: center

::

    # candlestick chart showing simple moving average
    # chart is saved as 'sma.png'
    import pynance as pn

    def run():
        eqdata = pn.data.get('TSLA', '2015', '2016')
        smadata = pn.tech.movave.sma(eqdata, selection='Close')
        pn.chart.candlestick(eqdata, title='TSLA 2015', fname='sma.png', sma=smadata)

    if __name__ == '__main__':
        run()
