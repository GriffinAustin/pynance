"""
Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import datetime as dt
import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestData(unittest.TestCase):

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
        self.optdata = pd.DataFrame(index=_index, columns=_columns)
        _n_rows = self.optdata.shape[0]
        self.optdata.loc[:, 'Last'] = np.arange(float(_n_rows))
        self.optdata.loc[:, 'Quote_Time'] = np.datetime64(dt.datetime(2015, 3, 1))
        self.optdata.loc[:, 'Underlying_Price'] = 10.1
        self.optdata.loc[:, 'Underlying'] = self.optdata.loc[:, 'Root'] = 'GE'
        self.optdata.loc[:, 'Chg'] = -.05
        self.optdata.loc[:, 'PctChg'] = '-11.3%'
        self.optdata.loc[:, 'Vol'] = 200
        self.optdata.loc[:, 'Open_Int'] = 400
        self.optdata.loc[:, 'IV'] = '18.0%'
        self.optdata.loc[:, 'IsNonstandard'] = False
        _callbids = [2.7, 2.8, 2.9, .9, 1., 1.1, .6, .7, .8]
        _putbids = [.6, .7, .8, .8, .9, 1., 2.5, 2.6, 2.7]
        _bids = np.array(sum(zip(_callbids, _putbids), ()))
        self.optdata.loc[:, 'Bid'] = _bids
        # setting ask as bid + .2 means that price is expected to be bid + .1
        self.optdata.loc[:, 'Ask'] = _bids + .2

    def test_get(self):
        # call in the money
        _opt, _eq, _qt, _tv = pn.opt.price.get(self.optdata, 'call', 8., '2015-05-01')
        self.assertAlmostEqual(_opt, 2.8)
        self.assertAlmostEqual(_eq, 10.1)
        self.assertEqual(_qt, dt.datetime(2015, 3, 1))
        self.assertAlmostEqual(_tv, .7)
        # call out of the money
        _opt, _, _, _tv = pn.opt.price.get(self.optdata, 'call', 12., '2015-06-01')
        self.assertAlmostEqual(_opt, .8)
        self.assertAlmostEqual(_tv, .8)
        # put in the money
        _opt, _, _, _tv = pn.opt.price.get(self.optdata, 'put', 12., '2015-07-01')
        self.assertAlmostEqual(_opt, 2.8)
        self.assertAlmostEqual(_tv, .9)
        # put out of the money
        _opt, _, _, _tv = pn.opt.price.get(self.optdata, 'put', 10., '2015-05-01')
        self.assertAlmostEqual(_opt, .9)
        self.assertAlmostEqual(_tv, .9)
        # without time value
        _opt, _eq, _qt = pn.opt.price.get(self.optdata, 'put', 10., '2015-06-01', showtimeval=False)
        self.assertAlmostEqual(_opt, 1.)
        self.assertAlmostEqual(_eq, 10.1)
        self.assertEqual(_qt, dt.datetime(2015, 3, 1))
        # exceptions
        self.assertRaises(KeyError, pn.opt.price.get, self.optdata, 'call', 10., '2015-06-02')

    def test_allstrikes(self):
        # call
        _opt, _eq, _qt = pn.opt.price.allstrikes(self.optdata, 'call', '2015-05-01')
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc[8., 'Price'], 2.8)
        self.assertAlmostEqual(_opt.loc[10., 'Price'], 1.)
        self.assertAlmostEqual(_opt.loc[12., 'Price'], .7)
        self.assertAlmostEqual(_opt.loc[8., 'Time_Val'], .7)
        self.assertAlmostEqual(_opt.loc[10., 'Time_Val'], .9)
        self.assertAlmostEqual(_opt.loc[12., 'Time_Val'], .7)
        self.assertAlmostEqual(_eq, 10.1)
        self.assertEqual(_qt, dt.datetime(2015, 3, 1))
        # put
        _opt, _, _ = pn.opt.price.allstrikes(self.optdata, 'put', '2015-06-01')
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc[8., 'Price'], .8)
        self.assertAlmostEqual(_opt.loc[10., 'Price'], 1.)
        self.assertAlmostEqual(_opt.loc[12., 'Price'], 2.7)
        self.assertAlmostEqual(_opt.loc[8., 'Time_Val'], .8)
        self.assertAlmostEqual(_opt.loc[10., 'Time_Val'], 1.)
        self.assertAlmostEqual(_opt.loc[12., 'Time_Val'], .8)
        # exceptions
        self.assertRaises(KeyError, pn.opt.price.allstrikes, self.optdata, 'call', '2015-06-30')

    def test_allexpiries(self):
        # call
        _opt, _eq, _qt = pn.opt.price.allexpiries(self.optdata, 'call', 8)
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Price'], 2.8)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Price'], 2.9)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Price'], 3.)
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Time_Val'], .7)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Time_Val'], .8)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Time_Val'], .9)
        # put
        _opt, _eq, _qt = pn.opt.price.allexpiries(self.optdata, 'put', 10)
        # only test price and time val for now
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Price'], .9)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Price'], 1.)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Price'], 1.1)
        self.assertAlmostEqual(_opt.loc['2015-05-01', 'Time_Val'], .9)
        self.assertAlmostEqual(_opt.loc['2015-06-01', 'Time_Val'], 1.)
        self.assertAlmostEqual(_opt.loc['2015-07-01', 'Time_Val'], 1.1)
        self.assertAlmostEqual(_eq, 10.1)
        self.assertEqual(_qt, dt.datetime(2015, 3, 1))
        # exceptions
        self.assertRaises(KeyError, pn.opt.price.allexpiries, self.optdata, 'call', 10.5)

if __name__ == '__main__':
    unittest.main()
