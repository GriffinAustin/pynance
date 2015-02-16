"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Unit tests for data module
"""

import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestData(unittest.TestCase):

    def setUp(self):
        session_dates = [
                '2014-01-06',
                '2014-01-07',
                '2014-01-08',
                '2014-01-09',
                '2014-01-10',
                '2014-01-13',
                '2014-01-14',
                '2014-01-15',
                '2014-01-16',
                '2014-01-17']
        self.equity_data = pd.DataFrame(np.arange(1., 21.).reshape((10, 2)), index=session_dates,
                columns=['Volume', 'Adj Close'])
        self.equity_data.index.name = 'Date'

    def test_ema(self):
        _span = 4
        _emadf = pn.tech.ema(self.equity_data.loc[:, 'Adj Close'], span=_span)
        _prev = _emadf.iloc[0, 0]
        # values are increasing but smaller than df values
        for i in range(1, len(_emadf.index)):
            self.assertTrue(_emadf.iloc[i, 0] < self.equity_data.iloc[i, 1])
            self.assertTrue(_emadf.iloc[i, 0] > _prev)
            _prev = _emadf.iloc[i, 0]
        # values are greater than 2 datapoints back in equity_data
        for i in range(2, len(_emadf.index)):
            self.assertTrue(_emadf.iloc[i, 0] > self.equity_data.iloc[i - 2, 1])

    def test_growth(self):
        # Defaults
        eqgrowth = pn.tech.growth(self.equity_data)
        self.assertEqual(eqgrowth.shape[0], self.equity_data.shape[0] - 1)
        self.assertEqual(eqgrowth.shape[1], 1)
        for i in range(9):
            self.assertAlmostEqual(eqgrowth.iloc[i, 0], (2. + i) / (1. + i))
            self.assertEqual(eqgrowth.index[i], self.equity_data.index[i + 1])
        # n_sessions=5, selection='Volume'
        eqgrowth = pn.tech.growth(self.equity_data, selection='Volume', n_sessions=5)
        self.assertEqual(eqgrowth.shape[0], self.equity_data.shape[0] - 5)
        self.assertEqual(eqgrowth.shape[1], 1)
        for i in range(5):
            self.assertAlmostEqual(eqgrowth.iloc[i, 0], (11. + 2. * i) / (1. + 2. * i))
            self.assertEqual(eqgrowth.index[i], self.equity_data.index[i + 5])

    def test_ret(self):
        # Defaults
        eqret = pn.tech.ret(self.equity_data)
        self.assertEqual(eqret.shape[0], self.equity_data.shape[0] - 1)
        self.assertEqual(eqret.shape[1], 1)
        for i in range(9):
            self.assertAlmostEqual(eqret.iloc[i, 0], 1. / (1. + i))
            self.assertEqual(eqret.index[i], self.equity_data.index[i + 1])
        # n_sessions=5, selection='Volume'
        eqret = pn.tech.ret(self.equity_data, selection='Volume', n_sessions=5)
        self.assertEqual(eqret.shape[0], self.equity_data.shape[0] - 5)
        self.assertEqual(eqret.shape[1], 1)
        for i in range(5):
            self.assertAlmostEqual(eqret.iloc[i, 0], 10. / (1. + 2. * i))
            self.assertEqual(eqret.index[i], self.equity_data.index[i + 5])

if __name__ == '__main__':
    unittest.main()
