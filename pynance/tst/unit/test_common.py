"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Unit tests for data module
"""

from functools import partial
import sys
import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestCommon(unittest.TestCase):

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
                columns=['Volume', 'Close'])
        self.equity_data.index.name = 'Date'

    def test_featurize_defaults(self):
        n_sessions = 3
        features = pn.featurize(self.equity_data, n_sessions)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_featurize_selection(self):
        n_sessions = 4
        features = pn.featurize(self.equity_data, n_sessions, selection='Volume')
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_featurize_columns(self):
        cols = [0, 1, 2, 3, 4]
        n_sessions = len(cols)
        features = pn.featurize(self.equity_data, n_sessions, columns=cols)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)
        for i in range(len(cols)):
            self.assertEqual(cols[i], features.columns.values[i])

    def test_decorate(self):
        def _f():
            return 0, 1
        self.assertEqual(pn.decorate(_f, 2, 3)(), (0, 1, 2, 3))
        self.assertEqual(pn.decorate(lambda x: x * 2, 0)(3), (6, 0))
        self.assertEqual(pn.decorate(lambda x: x, 4, 5)('foo'), ('foo', 4, 5))
        self.assertEqual(pn.decorate(_f, 'foo')(), (0, 1, 'foo'))
        _g = pn.decorate(_f, 2, foo='bar')
        self.assertEqual(_g.foo, 'bar')
        self.assertFalse(hasattr(_f, 'foo'))
        self.assertEqual(_g(), (0, 1, 2))

    def test_expand(self):
        def _f(eqdata):
            return 2. * eqdata
        _expanded_ret = pn.expand(_f, 'Close')(self.equity_data)
        self.assertEqual(len(_expanded_ret.values.flatten()), len(self.equity_data.index))
        for i in range(len(_expanded_ret.index)):
            self.assertEqual(_expanded_ret.index[i], self.equity_data.index[i])
            self.assertAlmostEqual(_expanded_ret.values[i], 4. + 4. * i) 

    def test_has_na(self):
        # dataframe
        # clean
        self.assertFalse(pn.has_na(self.equity_data))
        # None
        self.equity_data.iloc[0, 0] = None
        self.assertTrue(pn.has_na(self.equity_data))
        # np.nan
        self.equity_data.iloc[0, 0] = np.nan
        self.assertTrue(pn.has_na(self.equity_data))
        # ndarray
        _eqdata = np.arange(12.).reshape((3, 4))
        # clean
        self.assertFalse(pn.has_na(_eqdata))
        # None
        _eqdata[0, 0] = None
        self.assertTrue(pn.has_na(_eqdata))
        # np.nan
        _eqdata[0, 0] = np.nan
        self.assertTrue(pn.has_na(_eqdata))
        


if __name__ == '__main__':
    unittest.main()
