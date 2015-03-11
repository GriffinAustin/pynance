"""
Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import datetime as dt
import unittest

import numpy as np
import pandas as pd

import pynance as pn
from pynance.opt.core import Options

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
        _optdata = pd.DataFrame(index=_index, columns=_columns)
        _n_rows = _optdata.shape[0]
        _optdata.loc[:, 'Last'] = np.arange(float(_n_rows))
        _optdata.loc[:, 'Quote_Time'] = np.datetime64(dt.datetime(2015, 3, 1))
        _optdata.loc[:, 'Underlying_Price'] = 10.1
        _optdata.loc[:, 'Underlying'] = _optdata.loc[:, 'Root'] = 'GE'
        _optdata.loc[:, 'Chg'] = -.05
        _optdata.loc[:, 'PctChg'] = '-11.3%'
        _optdata.loc[:, 'Vol'] = 200
        _optdata.loc[:, 'Open_Int'] = 400
        _optdata.loc[:, 'IV'] = '18.0%'
        _optdata.loc[:, 'IsNonstandard'] = False
        _callbids = [2.7, 2.8, 2.9, .9, 1., 1.1, .6, .7, .8]
        _putbids = [.5, .6, .7, .8, .9, 1., 2.5, 2.6, 2.7]
        _bids = np.array(sum(zip(_callbids, _putbids), ()))
        _optdata.loc[:, 'Bid'] = _bids
        # setting ask as bid + .2 means that price is expected to be bid + .1
        _optdata.loc[:, 'Ask'] = _bids + .2
        self.options = Options(_optdata)

    def test_call(self):
        _df = self.options.spread.vert.call(8., 12., '2015-05-01')
        self.assertAlmostEqual(_df.loc['Low Strike Call', 'Value'], 2.8)
        self.assertAlmostEqual(_df.loc['High Strike Call', 'Value'], .7)
        self.assertAlmostEqual(_df.loc['Debit', 'Value'], 2.1)
        self.assertAlmostEqual(_df.loc['Max Profit', 'Value'], 1.9)
        self.assertAlmostEqual(_df.loc['Break_Even', 'Value'], 10.1)
        self.assertAlmostEqual(_df.loc['Underlying_Price', 'Value'], 10.1)
        self.assertEqual(_df.loc['Quote_Time', 'Value'], dt.datetime(2015, 3, 1))
        self.assertRaises(KeyError, self.options.spread.vert.call, 7.9, 12., '2015-05-01')
        self.assertRaises(KeyError, self.options.spread.vert.call, 8., 12.3, '2015-05-01')
        self.assertRaises(KeyError, self.options.spread.vert.call, 8., 12., '2015-05-27')

    def test_put(self):
        _df = self.options.spread.vert.put(8., 12., '2015-07-01')
        self.assertAlmostEqual(_df.loc['Low Strike Put', 'Value'], .8)
        self.assertAlmostEqual(_df.loc['High Strike Put', 'Value'], 2.8)
        self.assertAlmostEqual(_df.loc['Debit', 'Value'], 2.)
        self.assertAlmostEqual(_df.loc['Max Profit', 'Value'], 2.)
        self.assertAlmostEqual(_df.loc['Break_Even', 'Value'], 10.)
        self.assertAlmostEqual(_df.loc['Underlying_Price', 'Value'], 10.1)
        self.assertEqual(_df.loc['Quote_Time', 'Value'], dt.datetime(2015, 3, 1))
        self.assertRaises(KeyError, self.options.spread.vert.put, 7.9, 12., '2015-07-01')
        self.assertRaises(KeyError, self.options.spread.vert.put, 8., 12.3, '2015-07-01')
        self.assertRaises(KeyError, self.options.spread.vert.put, 8., 12., '2015-07-04')

    def test_straddle(self):
        _df = self.options.spread.vert.straddle(10., '2015-06-01')
        self.assertAlmostEqual(_df.loc['Call', 'Value'], 1.1)
        self.assertAlmostEqual(_df.loc['Put', 'Value'], 1.)
        self.assertAlmostEqual(_df.loc['Credit', 'Value'], 2.1)
        self.assertAlmostEqual(_df.loc['Underlying_Price', 'Value'], 10.1)
        self.assertEqual(_df.loc['Quote_Time', 'Value'], dt.datetime(2015, 3, 1))
        self.assertRaises(KeyError, self.options.spread.vert.straddle, 9.9, '2015-06-01')
             

if __name__ == '__main__':
    unittest.main()
