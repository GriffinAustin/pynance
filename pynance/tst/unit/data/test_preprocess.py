"""
Copyright (c) 2014, 2015 Marshall Farrier
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

class TestPreprocess(unittest.TestCase):

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

    def test_center_df(self):
        features = pd.DataFrame(data=np.random.random((112, 3)), columns=['1', '2', '3'])
        centered_features, feat_means = pn.data.center(features)
        means_of_centered = np.mean(centered_features.values, axis=0)
        for i in range(len(means_of_centered)):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertTrue(isinstance(centered_features, pd.DataFrame))
        self.assertTrue(isinstance(feat_means, pd.DataFrame))

    def test_center_partial_df(self):
        features = pd.DataFrame(data=np.ones((23, 4)), columns=map(str, range(4)), dtype='float64')
        features.iloc[:, 1:] = np.random.random((23, 3))
        centered_features, feat_means = pn.data.center(features.iloc[:, 1:], out=features.iloc[:, 1:])
        means_of_centered = np.mean(features.values, axis=0)
        self.assertAlmostEqual(means_of_centered[0], 1.)
        for i in range(1, len(means_of_centered)):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertTrue(isinstance(centered_features, pd.DataFrame))
        self.assertTrue(isinstance(feat_means, pd.DataFrame))

    def test_center_ndarray(self):
        features = np.random.random((27, 9))
        centered_features, feat_means = pn.data.center(features)
        means_of_centered = np.mean(centered_features, axis=0)
        for i in range(len(means_of_centered)):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertTrue(isinstance(centered_features, np.ndarray))
        self.assertTrue(isinstance(feat_means, np.ndarray))

    def test_center_ndarray_partial(self):
        features = np.ones((16, 5))
        features[:, :-1] = np.random.random((16, 4))
        centered_features, feat_means = pn.data.center(features[:, :-1], 
                out=features[:, :-1])
        means_of_centered = np.mean(features, axis=0)
        for i in range(len(means_of_centered) - 1):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertAlmostEqual(means_of_centered[-1], 1.)
        self.assertTrue(isinstance(centered_features, np.ndarray))
        self.assertTrue(isinstance(feat_means, np.ndarray))

    def test_normalize_df(self):
        features = pd.DataFrame(data=np.random.random((112, 3)), columns=['1', '2', '3'])
        centered_features, _ = pn.data.center(features)
        normalized_features, stds = pn.data.normalize(features)
        stds_of_normalized = np.std(normalized_features.values, axis=0)
        for i in range(len(stds_of_normalized)):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, pd.DataFrame))
        self.assertTrue(isinstance(stds, pd.DataFrame))

    def test_normalize_partial_df(self):
        features = pd.DataFrame(data=np.ones((23, 4)), columns=map(str, range(4)), dtype='float64')
        features.iloc[:, 1:] = np.random.random((23, 3))
        _, _ = pn.data.center(features.iloc[:, 1:], out=features.iloc[:, 1:])
        normalized_features, stds = pn.data.normalize(features.iloc[:, 1:], out=features.iloc[:, 1:])
        stds_of_normalized = np.std(features.values, axis=0)
        self.assertAlmostEqual(stds_of_normalized[0], 0.)
        for i in range(1, len(stds_of_normalized)):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, pd.DataFrame))
        self.assertTrue(isinstance(stds, pd.DataFrame))

    def test_normalize_ndarray(self):
        features = np.random.random((27, 9))
        centered_features, _ = pn.data.center(features)
        normalized_features, stds = pn.data.normalize(features)
        stds_of_normalized = np.std(normalized_features, axis=0)
        for i in range(len(stds_of_normalized)):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, np.ndarray))
        self.assertTrue(isinstance(stds, np.ndarray))

    def test_normalize_ndarray_partial(self):
        features = np.ones((16, 5))
        features[:, :-1] = np.random.random((16, 4))
        _, _ = pn.data.center(features[:, :-1], out=features[:, :-1])
        normalized_features, stds = pn.data.normalize(features[:, :-1], out=features[:, :-1])
        stds_of_normalized = np.std(features, axis=0)
        self.assertAlmostEqual(stds_of_normalized[-1], 0.)
        for i in range(len(stds_of_normalized) - 1):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, np.ndarray))
        self.assertTrue(isinstance(stds, np.ndarray))

    def test_transform_default(self):
        n_sessions = 3
        features = pn.featurize(self.equity_data, n_sessions)
        transformed = pn.data.transform(features)
        norms = np.linalg.norm(np.float64(transformed.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], 1.0)

    def test_transform_rows_vector(self):
        n_sessions = 3
        norm = 3.14159
        features = pn.featurize(self.equity_data, n_sessions)
        transformed = pn.data.transform(features, method="vector", norm=norm)
        norms = np.linalg.norm(np.float64(transformed.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)

    def test_transform_rows_mean(self):
        n_sessions = 3
        norm = 10.0
        features = pn.featurize(self.equity_data, n_sessions)
        transformed = pn.data.transform(features, method="mean", norm=norm, axis=0)
        means = transformed.mean(axis=1)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)

    def test_transform_rows_last(self):
        n_sessions = 3
        features = pn.featurize(self.equity_data, n_sessions)
        labels = pd.DataFrame(features.iloc[:, -1] * 0.5, index=features.index) 
        transformed_features, transformed_labels = pn.data.transform(features, method="last", labels=labels)
        for i in range(len(transformed_features.index)):
            self.assertAlmostEqual(transformed_features.iloc[i, -1], 1.0)
        for i in range(len(transformed_labels.index)):
            self.assertAlmostEqual(transformed_labels.iloc[i, 0], 0.5)

    def test_transform_rows_first(self):
        n_sessions = 3
        features = pn.featurize(self.equity_data, n_sessions)
        # 2 columns of labels
        labels = pd.DataFrame(index=features.index, columns=['Label1', 'Label2'])
        labels['Label1'] = features.iloc[:, 0] * 0.5
        labels['Label2'] = features.iloc[:, 0] * 2.0
        transformed_features, transformed_labels = pn.data.transform(features, method="first", labels=labels)
        for i in range(len(transformed_features.index)):
            self.assertAlmostEqual(transformed_features.iloc[i, 0], 1.0)
        for i in range(len(transformed_labels.index)):
            self.assertAlmostEqual(transformed_labels.iloc[i, 0], 0.5)
            self.assertAlmostEqual(transformed_labels.iloc[i, 1], 2.0)

    def test_transform_cols_vector(self):
        norm = 3.14159
        transformed = pn.data.transform(self.equity_data, method="vector", norm=norm, axis=1)
        norms = np.linalg.norm(np.float64(transformed.values), axis=0)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)
    
    def test_transform_cols_mean(self):
        norm = 10.0
        transformed = pn.data.transform(self.equity_data, method="mean", norm=norm, axis=1)
        means = transformed.mean(axis=0)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)
    
    def test_transform_cols_last(self):
        transformed = pn.data.transform(self.equity_data, method="last", axis=1)
        for i in range(len(transformed.columns)):
            self.assertAlmostEqual(transformed.iloc[-1, i], 1.0)
    
    def test_transform_cols_first(self):
        transformed = pn.data.transform(self.equity_data, method="first", axis=1)
        for i in range(len(transformed.columns)):
            self.assertAlmostEqual(transformed.iloc[0, i], 1.0)

if __name__ == '__main__':
    unittest.main()
