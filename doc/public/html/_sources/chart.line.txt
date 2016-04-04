PyNance chart example code: `close.py` and `adj_close.py`
=========================================================
`close.py`
----------

The following chart includes a stock split:

.. image:: /images/close.png
    :align: center

::

    # closing prices
    import pynance as pn

    def run():
        df = pn.data.get('GOOGL', '2014', '2015')
        pn.chart.close(df, title='GOOGL 2014')

    if __name__ == '__main__':
        run()

`adj_close.py`
--------------
*Adjusted close*, however, adjusts for splits and dividends:

.. image:: /images/adj_close.png
    :align: center

::

    # adjusted close
    import pynance as pn

    def run():
        df = pn.data.get('GOOGL', '2014', '2015')
        pn.chart.adj_close(df, title='GOOGL 2014')

    if __name__ == '__main__':
        run()
