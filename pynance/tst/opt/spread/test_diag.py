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
        self.opts = pn.opt.core.Options(_optdata)

    def test_dblcal(self):
        _df = self.opts.spread.diag.dblcal(8., 12., '2015-05-01', '2015-07-01')
        # calls
        self.assertAlmostEqual(_df.loc['Near Call', 'Value'], .7)
        self.assertAlmostEqual(_df.loc['Far Call', 'Value'], .9)
        self.assertAlmostEqual(_df.loc['Call Ratio', 'Value'], 7. / 9.)
        # puts
        self.assertAlmostEqual(_df.loc['Near Put', 'Value'], .6)
        self.assertAlmostEqual(_df.loc['Far Put', 'Value'], .8)
        self.assertAlmostEqual(_df.loc['Put Ratio', 'Value'], .75)
        # other
        self.assertAlmostEqual(_df.loc['Debit', 'Value'], .4)
        self.assertAlmostEqual(_df.loc['Underlying_Price', 'Value'], 10.1)
        self.assertEqual(_df.loc['Quote_Time', 'Value'], dt.datetime(2015, 3, 1))
        # exceptions
        self.assertRaises(KeyError, self.opts.spread.diag.dblcal, 8., 11.9,
                '2015-05-01', '2015-07-01')
        self.assertRaises(KeyError, self.opts.spread.diag.dblcal, 10., 12.,
                '2015-05-01', '2015-06-15')

    def test_diagbtrfly(self):
        _df = self.opts.spread.diag.diagbtrfly(8., 10., 12., '2015-06-01', '2015-07-01')
        # near
        self.assertAlmostEqual(_df.loc['Straddle Call', 'Value'], 1.1)
        self.assertAlmostEqual(_df.loc['Straddle Put', 'Value'], 1.)
        self.assertAlmostEqual(_df.loc['Straddle Total', 'Value'], 2.1)
        # far
        self.assertAlmostEqual(_df.loc['Far Call', 'Value'], .9)
        self.assertAlmostEqual(_df.loc['Far Put', 'Value'], .8)
        self.assertAlmostEqual(_df.loc['Far Total', 'Value'], 1.7)
        # other
        self.assertAlmostEqual(_df.loc['Straddle to Far Ratio', 'Value'], 21. / 17.)
        self.assertAlmostEqual(_df.loc['Underlying_Price', 'Value'], 10.1)
        self.assertEqual(_df.loc['Quote_Time', 'Value'], dt.datetime(2015, 3, 1))
        #exceptions
        self.assertRaises(KeyError, self.opts.spread.diag.diagbtrfly, 8., 10., 11.9, 
                '2015-06-01', '2015-07-01')
        self.assertRaises(KeyError, self.opts.spread.diag.diagbtrfly, 8., 10., 12., 
                '2015-06-11', '2015-07-01')

if __name__ == '__main__':
    unittest.main()
