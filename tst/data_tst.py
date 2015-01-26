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

    def test_feat_featurize_defaults(self):
        n_sessions = 3
        features = data.feat.featurize(self.equity_data, n_sessions)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_feat_featurize_selection(self):
        n_sessions = 4
        features = data.feat.featurize(self.equity_data, n_sessions, selection='Volume')
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)

    def test_feat_featurize_columns(self):
        cols = ['one', 'two', 'three']
        n_sessions = len(cols)
        features = data.feat.featurize(self.equity_data, n_sessions, columns=cols)
        self.assertEqual(len(features.index), len(self.equity_data.index) - n_sessions + 1)
        self.assertEqual(len(features.columns), n_sessions)
        for i in range(len(cols)):
            self.assertEqual(cols[i], features.columns.values[i])

    def test_center_df(self):
        features = pd.DataFrame(data=np.random.random((112, 3)), columns=['1', '2', '3'])
        centered_features, feat_means = data.center(features)
        means_of_centered = np.mean(centered_features.values, axis=0)
        for i in range(len(means_of_centered)):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertTrue(isinstance(centered_features, pd.DataFrame))
        self.assertTrue(isinstance(feat_means, pd.DataFrame))

    def test_center_partial_df(self):
        features = pd.DataFrame(data=np.ones((23, 4)), columns=map(str, range(4)), dtype='float64')
        features.iloc[:, 1:] = np.random.random((23, 3))
        centered_features, feat_means = data.center(features.iloc[:, 1:], out=features.iloc[:, 1:])
        means_of_centered = np.mean(features.values, axis=0)
        self.assertAlmostEqual(means_of_centered[0], 1.)
        for i in range(1, len(means_of_centered)):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertTrue(isinstance(centered_features, pd.DataFrame))
        self.assertTrue(isinstance(feat_means, pd.DataFrame))

    def test_center_ndarray(self):
        features = np.random.random((27, 9))
        centered_features, feat_means = data.center(features)
        means_of_centered = np.mean(centered_features, axis=0)
        for i in range(len(means_of_centered)):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertTrue(isinstance(centered_features, np.ndarray))
        self.assertTrue(isinstance(feat_means, np.ndarray))

    def test_center_ndarray_partial(self):
        features = np.ones((16, 5))
        features[:, :-1] = np.random.random((16, 4))
        centered_features, feat_means = data.center(features[:, :-1], 
                out=features[:, :-1])
        means_of_centered = np.mean(features, axis=0)
        for i in range(len(means_of_centered) - 1):
            self.assertAlmostEqual(means_of_centered[i], 0.)
        self.assertAlmostEqual(means_of_centered[-1], 1.)
        self.assertTrue(isinstance(centered_features, np.ndarray))
        self.assertTrue(isinstance(feat_means, np.ndarray))

    def test_normalize_df(self):
        features = pd.DataFrame(data=np.random.random((112, 3)), columns=['1', '2', '3'])
        centered_features, _ = data.center(features)
        normalized_features, stds = data.normalize(features)
        stds_of_normalized = np.std(normalized_features.values, axis=0)
        for i in range(len(stds_of_normalized)):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, pd.DataFrame))
        self.assertTrue(isinstance(stds, pd.DataFrame))

    def test_normalize_partial_df(self):
        features = pd.DataFrame(data=np.ones((23, 4)), columns=map(str, range(4)), dtype='float64')
        features.iloc[:, 1:] = np.random.random((23, 3))
        _, _ = data.center(features.iloc[:, 1:], out=features.iloc[:, 1:])
        normalized_features, stds = data.normalize(features.iloc[:, 1:], out=features.iloc[:, 1:])
        stds_of_normalized = np.std(features.values, axis=0)
        self.assertAlmostEqual(stds_of_normalized[0], 0.)
        for i in range(1, len(stds_of_normalized)):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, pd.DataFrame))
        self.assertTrue(isinstance(stds, pd.DataFrame))

    def test_normalize_ndarray(self):
        features = np.random.random((27, 9))
        centered_features, _ = data.center(features)
        normalized_features, stds = data.normalize(features)
        stds_of_normalized = np.std(normalized_features, axis=0)
        for i in range(len(stds_of_normalized)):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, np.ndarray))
        self.assertTrue(isinstance(stds, np.ndarray))

    def test_normalize_ndarray_partial(self):
        features = np.ones((16, 5))
        features[:, :-1] = np.random.random((16, 4))
        _, _ = data.center(features[:, :-1], out=features[:, :-1])
        normalized_features, stds = data.normalize(features[:, :-1], out=features[:, :-1])
        stds_of_normalized = np.std(features, axis=0)
        self.assertAlmostEqual(stds_of_normalized[-1], 0.)
        for i in range(len(stds_of_normalized) - 1):
            self.assertAlmostEqual(stds_of_normalized[i], 1.)
        self.assertTrue(isinstance(normalized_features, np.ndarray))
        self.assertTrue(isinstance(stds, np.ndarray))

    def test_transform_default(self):
        n_sessions = 3
        features = data.feat.featurize(self.equity_data, n_sessions)
        transformed = data.transform(features)
        norms = np.linalg.norm(np.float64(transformed.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], 1.0)

    def test_transform_rows_vector(self):
        n_sessions = 3
        norm = 3.14159
        features = data.feat.featurize(self.equity_data, n_sessions)
        transformed = data.transform(features, method="vector", norm=norm)
        norms = np.linalg.norm(np.float64(transformed.values), axis=1)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)

    def test_transform_rows_mean(self):
        n_sessions = 3
        norm = 10.0
        features = data.feat.featurize(self.equity_data, n_sessions)
        transformed = data.transform(features, method="mean", norm=norm, axis=0)
        means = transformed.mean(axis=1)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)

    def test_transform_rows_last(self):
        n_sessions = 3
        features = data.feat.featurize(self.equity_data, n_sessions)
        labels = pd.DataFrame(features.iloc[:, -1] * 0.5, index=features.index) 
        transformed_features, transformed_labels = data.transform(features, method="last", labels=labels)
        for i in range(len(transformed_features.index)):
            self.assertAlmostEqual(transformed_features.iloc[i, -1], 1.0)
        for i in range(len(transformed_labels.index)):
            self.assertAlmostEqual(transformed_labels.iloc[i, 0], 0.5)

    def test_transform_rows_first(self):
        n_sessions = 3
        features = data.feat.featurize(self.equity_data, n_sessions)
        # 2 columns of labels
        labels = pd.DataFrame(index=features.index, columns=['Label1', 'Label2'])
        labels['Label1'] = features.iloc[:, 0] * 0.5
        labels['Label2'] = features.iloc[:, 0] * 2.0
        transformed_features, transformed_labels = data.transform(features, method="first", labels=labels)
        for i in range(len(transformed_features.index)):
            self.assertAlmostEqual(transformed_features.iloc[i, 0], 1.0)
        for i in range(len(transformed_labels.index)):
            self.assertAlmostEqual(transformed_labels.iloc[i, 0], 0.5)
            self.assertAlmostEqual(transformed_labels.iloc[i, 1], 2.0)

    def test_transform_cols_vector(self):
        norm = 3.14159
        transformed = data.transform(self.equity_data, method="vector", norm=norm, axis=1)
        norms = np.linalg.norm(np.float64(transformed.values), axis=0)
        for i in range(len(norms)):
            self.assertAlmostEqual(norms[i], norm)
    
    def test_transform_cols_mean(self):
        norm = 10.0
        transformed = data.transform(self.equity_data, method="mean", norm=norm, axis=1)
        means = transformed.mean(axis=0)
        for i in range(len(means)):
            self.assertAlmostEqual(means.iloc[i], norm)
    
    def test_transform_cols_last(self):
        transformed = data.transform(self.equity_data, method="last", axis=1)
        for i in range(len(transformed.columns)):
            self.assertAlmostEqual(transformed.iloc[-1, i], 1.0)
    
    def test_transform_cols_first(self):
        transformed = data.transform(self.equity_data, method="first", axis=1)
        for i in range(len(transformed.columns)):
            self.assertAlmostEqual(transformed.iloc[0, i], 1.0)

    def test_feat_add_const_df(self):
        n_sessions = 3
        features = data.feat.featurize(self.equity_data, n_sessions)
        x = data.feat.add_const(features)
        self.assertTrue(isinstance(x, pd.DataFrame))
        self.assertFalse(isinstance(x, np.ndarray))
        self.assertEqual(len(x.index), len(features.index))
        self.assertEqual(len(x.columns), len(features.columns) + 1)
        for i in range(len(x.index)):
            self.assertAlmostEqual(x.iloc[i, 0], 1.0)
            for j in range(len(features.columns)):
                self.assertAlmostEqual(x.iloc[i, j + 1], features.iloc[i, j])
    
    def test_feat_add_const_ndarray(self):
        n_sessions = 3
        features = data.feat.featurize(self.equity_data, n_sessions).values
        x = data.feat.add_const(features)
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertFalse(isinstance(x, pd.DataFrame))
        self.assertEqual(x.shape[0], features.shape[0])
        self.assertEqual(x.shape[1], features.shape[1] + 1)
        for i in range(x.shape[0]):
            self.assertAlmostEqual(x[i, 0], 1.0)
            for j in range(features.shape[1]):
                self.assertAlmostEqual(x[i, j + 1], features[i, j])

    def test_feat_growth(self):
        # Defaults
        eqgrowth = data.feat.growth(self.equity_data)
        self.assertEqual(eqgrowth.shape[0], self.equity_data.shape[0] - 1)
        self.assertEqual(eqgrowth.shape[1], 1)
        for i in range(9):
            self.assertAlmostEqual(eqgrowth.iloc[i, 0], (2. + i) / (1. + i))
            self.assertEqual(eqgrowth.index[i], self.equity_data.index[i + 1])
        # n_sessions=5, selection='Volume'
        eqgrowth = data.feat.growth(self.equity_data, selection='Volume', n_sessions=5)
        self.assertEqual(eqgrowth.shape[0], self.equity_data.shape[0] - 5)
        self.assertEqual(eqgrowth.shape[1], 1)
        for i in range(5):
            self.assertAlmostEqual(eqgrowth.iloc[i, 0], (11. + 2. * i) / (1. + 2. * i))
            self.assertEqual(eqgrowth.index[i], self.equity_data.index[i + 5])

    def test_feat_ret(self):
        # Defaults
        eqret = data.feat.ret(self.equity_data)
        self.assertEqual(eqret.shape[0], self.equity_data.shape[0] - 1)
        self.assertEqual(eqret.shape[1], 1)
        for i in range(9):
            self.assertAlmostEqual(eqret.iloc[i, 0], 1. / (1. + i))
            self.assertEqual(eqret.index[i], self.equity_data.index[i + 1])
        # n_sessions=5, selection='Volume'
        eqret = data.feat.ret(self.equity_data, selection='Volume', n_sessions=5)
        self.assertEqual(eqret.shape[0], self.equity_data.shape[0] - 5)
        self.assertEqual(eqret.shape[1], 1)
        for i in range(5):
            self.assertAlmostEqual(eqret.iloc[i, 0], 10. / (1. + 2. * i))
            self.assertEqual(eqret.index[i], self.equity_data.index[i + 5])

    def test_labeledfeatures(self):
        features, labels = data.labeledfeatures(self.equity_data, 2, 
                partial(data.lab.growth, 1, 'Adj Close'), averaging_interval=3)
        self.assertEqual(features.values.shape[0], labels.values.shape[0])
        self.assertEqual(features.values.shape[1], 5)
        for i in range(1, len(features.index)):
            self.assertAlmostEqual(features.loc[:, '-1G'].values[i], 
                    features.loc[:, '0G'].values[i - 1])
            self.assertAlmostEqual(features.loc[:, '-1V'].values[i], 
                    features.loc[:, '0V'].values[i - 1])
        for i in range(5):
            self.assertAlmostEqual(features.loc[:, '0G'].values[i], (i + 5.) / (i + 4.))
            self.assertAlmostEqual(features.loc[:, '0V'].values[i], (2. * i + 9.) / (2. * i + 5.))
            self.assertAlmostEqual(labels.values[i], (i + 6.) / (i + 5.))

    def test_labels_growth(self):
        prediction_interval = 2
        labels, skipatend = data.lab.growth(prediction_interval, 'Adj Close', self.equity_data)
        self.assertEqual(skipatend, prediction_interval)
        self.assertEqual(len(labels.index), len(self.equity_data.index) - prediction_interval)
        for i in range(len(labels.index)):
            self.assertAlmostEqual(labels.values[i], (i + 3.) / (i + 1.))

if __name__ == '__main__':
    unittest.main()
