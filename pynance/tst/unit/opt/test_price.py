"""
Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import datetime as dt
import unittest

import numpy as np
import pandas as pd
from pytz import timezone

import pynance as pn

class TestPrice(unittest.TestCase):

    def setUp(self):
        # We need at least 3 dates, 3 strikes, both calls and puts
        _indexnames = ['Strike', 'Expiry', 'Type', 'Symbol']
        _iterables = [
                [8., 10., 12.],
                [dt.datetime(2015, 5, 1), dt.datetime(2015, 6, 1), dt.datetime(2015, 7, 1)],
                ['call', 'put'],
                ['blah140x01CP']]
        _index = pd.MultiIndex.from_product(_iterables, names=_indexnames)
        _columns = ['Last', 'Bid', 'Ask', 'Chg', 'PctChg', 'Vol', 'Open_Int', 'IV', 'Root', 
                'IsNonstandard', 'Underlying', 'Underlying_Price', 'Quote_Time']
        _optdata = pd.DataFrame(index=_index, columns=_columns)
        _n_rows = _optdata.shape[0]
        _optdata.loc[:, 'Last'] = np.arange(float(_n_rows))
        _optdata.loc[:, 'Quote_Time'] = np.datetime64(dt.datetime(2015, 3, 1, 16, tzinfo=timezone('US/Eastern')))
        _optdata.loc[:, 'Underlying_Price'] = 10.1
        _optdata.loc[:, 'Underlying'] = _optdata.loc[:, 'Root'] = 'GE'
        _optdata.loc[:, 'Chg'] = -.05
        _optdata.loc[:, 'PctChg'] = '-11.3%'
        _optdata.loc[:, 'Vol'] = 200
        _optdata.loc[:, 'Open_Int'] = 400
        _optdata.loc[:, 'IV'] = '18.0%'
        _optdata.loc[:, 'IsNonstandard'] = False
        _callbids = [2.7, 2.8, 2.9, .9, 1., 1.1, .6, .7, .8]
        _putbids = [.6, .7, .8, .8, .9, 1., 2.5, 2.6, 2.7]
        _bids = np.array(sum(zip(_callbids, _putbids), ()))
        _optdata.loc[:, 'Bid'] = _bids
        # setting ask as bid + .2 means that price is expected to be bid + .1
        _optdata.loc[:, 'Ask'] = _bids + .2
        self.opts = pn.opt.core.Options(_optdata)
        self.price = pn.opt.price.Price(_optdata)

    def test_get(self):
        # call
        self.assertAlmostEqual(self.opts.price.get('call', 8., '2015-05-01'), 2.8)
        # put
        self.assertAlmostEqual(self.opts.price.get('put', 10., '2015-05-01'), .9)

    def test_metrics(self):
        # call in the money
        _df = self.opts.price.metrics('call', 8., '2015-05-01')
        self.assertAlmostEqual(_df.loc['Opt_Price', 'Value'], 2.8)
        self.assertAlmostEqual(_df.loc['Time_Val', 'Value'], .7)
        self.assertAlmostEqual(_df.loc['Last', 'Value'], 0.)
        self.assertAlmostEqual(_df.loc['Bid', 'Value'], 2.7)
        self.assertAlmostEqual(_df.loc['Ask', 'Value'], 2.9)
        self.assertEqual(_df.loc['Vol', 'Value'], 200)
        self.assertEqual(_df.loc['Open_Int', 'Value'], 400)
        self.assertAlmostEqual(_df.loc['Underlying_Price', 'Value'], 10.1)
        # Cf. https://github.com/numpy/numpy/issues/5761
        # self.assertEqual(_df.loc['Quote_Time', 'Value'], np.datetime64(dt.datetime(2015, 3, 1, 16, tzinfo=timezone('US/Eastern'))))
        # call out of the money
        _df = self.opts.price.metrics('call', 12., '2015-06-01')
        self.assertAlmostEqual(_df.loc['Opt_Price', 'Value'], .8)
        self.assertAlmostEqual(_df.loc['Time_Val', 'Value'], .8)
        self.assertAlmostEqual(_df.loc['Last', 'Value'], 14.)
        # put in the money
        _df = self.opts.price.metrics('put', 12., '2015-07-01')
        self.assertAlmostEqual(_df.loc['Opt_Price', 'Value'], 2.8)
        self.assertAlmostEqual(_df.loc['Time_Val', 'Value'], .9)
        # put out of the money
        _df = self.opts.price.metrics('put', 10., '2015-05-01')
        self.assertAlmostEqual(_df.loc['Opt_Price', 'Value'], .9)
        self.assertAlmostEqual(_df.loc['Time_Val', 'Value'], .9)
        # exceptions
        self.assertRaises(KeyError, self.opts.price.metrics, 'call', 10., '2015-06-02')

    def test_strikes(self):
        # call
        _opt, _eq, _qt = self.opts.price.strikes('call', '2015-05-01')
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc[8., 'Price'], 2.8)
        self.assertAlmostEqual(_opt.loc[10., 'Price'], 1.)
        self.assertAlmostEqual(_opt.loc[12., 'Price'], .7)
        self.assertAlmostEqual(_opt.loc[8., 'Time_Val'], .7)
        self.assertAlmostEqual(_opt.loc[10., 'Time_Val'], .9)
        self.assertAlmostEqual(_opt.loc[12., 'Time_Val'], .7)
        self.assertAlmostEqual(_eq, 10.1)
        self.assertEqual(_qt, dt.datetime(2015, 3, 1, 16, tzinfo=timezone('US/Eastern')))
        # put
        _opt, _, _ = self.opts.price.strikes('put', '2015-06-01')
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc[8., 'Price'], .8)
        self.assertAlmostEqual(_opt.loc[10., 'Price'], 1.)
        self.assertAlmostEqual(_opt.loc[12., 'Price'], 2.7)
        self.assertAlmostEqual(_opt.loc[8., 'Time_Val'], .8)
        self.assertAlmostEqual(_opt.loc[10., 'Time_Val'], 1.)
        self.assertAlmostEqual(_opt.loc[12., 'Time_Val'], .8)
        # exceptions
        self.assertRaises(KeyError, self.opts.price.strikes, 'call', '2015-06-30')

    def test_exps(self):
        # call
        _opt, _eq, _qt = self.opts.price.exps('call', 8)
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Price'], 2.8)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Price'], 2.9)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Price'], 3.)
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Time_Val'], .7)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Time_Val'], .8)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Time_Val'], .9)
        # put
        _opt, _eq, _qt = self.opts.price.exps('put', 10)
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Price'], .9)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Price'], 1.)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Price'], 1.1)
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Time_Val'], .9)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Time_Val'], 1.)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Time_Val'], 1.1)
        self.assertAlmostEqual(_eq, 10.1)
        self.assertEqual(_qt, dt.datetime(2015, 3, 1, 16, tzinfo=timezone('US/Eastern')))
        # exceptions
        self.assertRaises(KeyError, self.opts.price.exps, 'call', 10.5)

if __name__ == '__main__':
    unittest.main()
