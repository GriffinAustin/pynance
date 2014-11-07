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

    def test_featurize_defaults(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_featurize_selection(self):
        n_sessions = 4
        features = data.featurize(self.equity_data, n_sessions, selection='Volume')
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_featurize_columns(self):
        cols = ['one', 'two', 'three']
        n_sessions = len(cols)
        features = data.featurize(self.equity_data, n_sessions, columns=cols)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)
        for i in range(len(cols)):
            self.assertEqual(cols[i], features.columns.values[i])

    def test_normalize_default(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features)
        norms = np.linalg.norm(np.float64(normalized.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], 1.0)

    def test_normalize_rows_vector(self):
        n_sessions = 3
        norm = 3.14159
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features, method="vector", norm=norm)
        norms = np.linalg.norm(np.float64(normalized.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)

    def test_normalize_rows_mean(self):
        n_sessions = 3
        norm = 10.0
        features = data.featurize(self.equity_data, n_sessions)
        normalized = data.normalize(features, method="mean", norm=norm, axis=0)
        means = normalized.mean(axis=1)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)

    def test_normalize_rows_last(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        labels = pd.DataFrame(features.iloc[:, -1] * 0.5, index=features.index) 
        normalized_features, normalized_labels = data.normalize(features, method="last", labels=labels)
        for i in range(len(normalized_features.index)):
            self.assertAlmostEqual(normalized_features.iloc[i, -1], 1.0)
        for i in range(len(normalized_labels.index)):
            self.assertAlmostEqual(normalized_labels.iloc[i, 0], 0.5)

    def test_normalize_rows_first(self):
        n_sessions = 3
        features = data.featurize(self.equity_data, n_sessions)
        # 2 columns of labels
        labels = pd.DataFrame(index=features.index, columns=['Label1', 'Label2'])
        labels['Label1'] = features.iloc[:, 0] * 0.5
        labels['Label2'] = features.iloc[:, 0] * 2.0
        normalized_features, normalized_labels = data.normalize(features, method="first", labels=labels)
        for i in range(len(normalized_features.index)):
            self.assertAlmostEqual(normalized_features.iloc[i, 0], 1.0)
        for i in range(len(normalized_labels.index)):
            self.assertAlmostEqual(normalized_labels.iloc[i, 0], 0.5)
            self.assertAlmostEqual(normalized_labels.iloc[i, 1], 2.0)

    def test_normalize_cols_vector(self):
        norm = 3.14159
        normalized = data.normalize(self.equity_data, method="vector", norm=norm, axis=1)
        norms = np.linalg.norm(np.float64(normalized.values), axis=0)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)
    
    def test_normalize_cols_mean(self):
        norm = 10.0
        normalized = data.normalize(self.equity_data, method="mean", norm=norm, axis=1)
        means = normalized.mean(axis=0)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)
    
    def test_normalize_cols_last(self):
        normalized = data.normalize(self.equity_data, method="last", axis=1)
        for i in range(len(normalized.columns)):
            self.assertAlmostEqual(normalized.iloc[-1, i], 1.0)
    
    def test_normalize_cols_first(self):
        normalized = data.normalize(self.equity_data, method="first", axis=1)
        for i in range(len(normalized.columns)):
            self.assertAlmostEqual(normalized.iloc[0, i], 1.0)
    
if __name__ == '__main__':
    unittest.main()
