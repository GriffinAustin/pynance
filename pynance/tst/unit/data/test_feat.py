"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Unit tests for data module
"""

from functools import partial
import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestFeat(unittest.TestCase):

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

    def test_add_const_df(self):
        n_sessions = 3
        features = pn.featurize(self.equity_data, n_sessions)
        x = pn.data.feat.add_const(features)
        self.assertTrue(isinstance(x, pd.DataFrame))
        self.assertFalse(isinstance(x, np.ndarray))
        self.assertEqual(len(x.index), len(features.index))
        self.assertEqual(len(x.columns), len(features.columns) + 1)
        for i in range(len(x.index)):
            self.assertAlmostEqual(x.iloc[i, 0], 1.0)
            for j in range(len(features.columns)):
                self.assertAlmostEqual(x.iloc[i, j + 1], features.iloc[i, j])
    
    def test_add_const_ndarray(self):
        n_sessions = 3
        features = pn.featurize(self.equity_data, n_sessions).values
        x = pn.data.feat.add_const(features)
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertFalse(isinstance(x, pd.DataFrame))
        self.assertEqual(x.shape[0], features.shape[0])
        self.assertEqual(x.shape[1], features.shape[1] + 1)
        for i in range(x.shape[0]):
            self.assertAlmostEqual(x[i, 0], 1.0)
            for j in range(features.shape[1]):
                self.assertAlmostEqual(x[i, j + 1], features[i, j])

    def test_fromcols(self):
        _selection = ['Close', 'Volume']
        _n_sess = 2
        # with constant feature (default)
        _features = pn.data.feat.fromcols(_selection, _n_sess, self.equity_data)
        self.assertEqual(len(_features.index), len(self.equity_data.index) - _n_sess + 1)
        for i in range(len(_features.index)):
            self.assertAlmostEqual(_features.iloc[i, 0], 1.)
            self.assertEqual(_features.index[i], self.equity_data.index[i + _n_sess - 1])
            for j in range(_n_sess):
                self.assertAlmostEqual(_features.iloc[i, j + 1], 2. + 2. * (i + j))
                self.assertAlmostEqual(_features.iloc[i, _n_sess + j + 1], 1. + 2. * (i + j))
        # no constant feature
        _constfeat = False
        _features = pn.data.feat.fromcols(_selection, _n_sess, self.equity_data, constfeat=_constfeat)
        self.assertEqual(len(_features.index), len(self.equity_data.index) - _n_sess + 1)
        for i in range(len(_features.index)):
            self.assertEqual(_features.index[i], self.equity_data.index[i + _n_sess - 1])
            for j in range(_n_sess):
                self.assertAlmostEqual(_features.iloc[i, j], 2. + 2. * (i + j))
                self.assertAlmostEqual(_features.iloc[i, _n_sess + j], 1. + 2. * (i + j))

    def test_fromfuncs(self):
        _vol_ave_int = 2
        _sma_window = 4
        _skipatstart = _sma_window - 1
        _n_sess = 3
        _smafunc = pn.expand(pn.tech.sma, 'Close')
        _funcs = [
                pn.decorate(partial(pn.tech.ratio_to_ave, _vol_ave_int),
                    title='MyRelVol'),
                pn.decorate(partial(_smafunc, window=_sma_window), title='MySMA')]
        _features = pn.data.feat.fromfuncs(_funcs, _n_sess, self.equity_data, 
                skipatstart=_skipatstart) 
        self.assertEqual(len(_features.index), len(self.equity_data.index) - _n_sess - _skipatstart + 1)
        for i in range(len(_features.index)):
            self.assertAlmostEqual(_features.iloc[i, 0], 1.)
            self.assertEqual(_features.index[i], self.equity_data.index[i + _n_sess + _skipatstart - 1])
            for j in range(_n_sess):
                # relative volumes all between 1.0 and 2.0
                self.assertTrue(_features.iloc[i, j + 1] < 2.)
                self.assertTrue(_features.iloc[i, j + 1] > 1.)
                # SMAs are means of values like 4, 6, 8, 10
                self.assertAlmostEqual(_features.iloc[i, j + _n_sess + 1], 1. + _sma_window + 2. * (i + j)) 
            # properties of relative volumes
            if i >= 1:
                # strictly decreasing
                self.assertTrue(_features.iloc[i, 1] < _features.iloc[i - 1, 1])
                # columns match with offset
                self.assertAlmostEqual(_features.iloc[i, 1], _features.iloc[i - 1, 2])
                self.assertAlmostEqual(_features.iloc[i, 2], _features.iloc[i - 1, 3])
        

if __name__ == '__main__':
    unittest.main()
