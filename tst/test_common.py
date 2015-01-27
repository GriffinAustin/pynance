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
        cols = ['one', 'two', 'three']
        n_sessions = len(cols)
        features = pn.featurize(self.equity_data, n_sessions, columns=cols)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)
        for i in range(len(cols)):
            self.assertEqual(cols[i], features.columns.values[i])

if __name__ == '__main__':
    unittest.main()
