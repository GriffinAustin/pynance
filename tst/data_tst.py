"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Unit tests for data module
"""

import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append('../pynance')
import data

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

    def test_featurize_default_col(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_featurize_col_arg(self):
        n_sessions = 4
        features = data.featurize(self.equity_data, n_sessions, column='Volume')
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_normalize_default(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features)
        norms = np.linalg.norm(np.float64(normalized.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], 1.0)

    def test_normalize_vector(self):
        n_sessions = 3
        norm = 3.14159
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features, method="vector", norm=norm)
        norms = np.linalg.norm(np.float64(normalized.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)

    def test_normalize_mean(self):
        n_sessions = 3
        norm = 10.0
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features, method="mean", norm=norm)
        means = normalized.mean(axis=1)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)

    def test_normalize_last(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features, method="last")
        for i in range(len(normalized.index)):
            self.assertAlmostEqual(normalized.iloc[i, -1], 1.0)

    def test_normalize_first(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features, method="first")
        for i in range(len(normalized.index)):
            self.assertAlmostEqual(normalized.iloc[i, 0], 1.0)

if __name__ == '__main__':
    unittest.main()
