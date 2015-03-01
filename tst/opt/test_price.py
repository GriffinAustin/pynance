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
                [dt.datetime(2014, 5, 1), dt.datetime(2014, 6, 1), dt.datetime(2014, 7, 1)],
                ['call', 'put'],
                ['blah140x01CP']]
        _index = pd.MultiIndex.from_product(_iterables, names=_indexnames)
        _columns = ['Last', 'Bid', 'Ask', 'Chg', 'PctChg', 'Vol', 'Open_Int', 'IV', 'Root', 
                'IsNonstandard', 'Underlying', 'Underlying_Price', 'Quote_Time']
        self.optdata = pd.DataFrame(index=_index, columns=_columns)
        _n_rows = self.optdata.shape[0]
        self.optdata.loc[:, 'Last'] = np.arange(float(_n_rows))
        self.optdata.loc[:, 'Quote_Time'] = np.datetime64(dt.datetime(2015, 3, 1))
        self.optdata.loc[:, 'Underlying_Price'] = 10.11
        self.optdata.loc[:, 'Underlying'] = self.optdata.loc[:, 'Root'] = 'GE'
        self.optdata.loc[:, 'Chg'] = -.05
        self.optdata.loc[:, 'PctChg'] = '-11.3%'
        self.optdata.loc[:, 'Vol'] = 200
        self.optdata.loc[:, 'Open_Int'] = 400
        self.optdata.loc[:, 'IV'] = '18.0%'
        self.optdata.loc[:, 'IsNonstandard'] = False

    def test_get(self):
        print(self.optdata)
        print(pn.opt.price.get(self.optdata, 'put', 10., '2014-06-01'))

if __name__ == '__main__':
    unittest.main()
