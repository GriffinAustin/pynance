"""
Copyright (c) 2015-2016 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2016-01-28
@summary: Unit tests for linear regression
"""

import os
import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestLinReg(unittest.TestCase):

    def ndarr_almost_eq(self, a, b, msg=None):
        if not np.allclose(a, b):
            print('ndarrays not equal:')
            print(a)
            print(b)
            raise self.failureException(msg)

    def test_run_noreg(self):
        features, labels = get_yule_data()
        model = pn.learn.linreg.run(features.values, labels.values)
        expected_model = [12.88, .75, .06, -.31]
        for actual, expected in zip(model.flatten().tolist(), expected_model):
            self.assertAlmostEqual(actual, expected, places=2)

    def test_beats_yule(self):
        # Yule's values are slightly different
        features, labels = get_yule_data()
        models = {}
        predicted = {}
        errors = {}
        models['ours'] = pn.learn.linreg.run(features.values, labels.values)
        models['yule'] = np.array([13.19, 0.755, -.022, -.322]).reshape((4, 1))
        for key in models:
            predicted[key] = pn.learn.linreg.predict(features, models[key])
            errors[key] = pn.learn.mse(predicted[key], labels)
        self.assertLessEqual(errors['ours'][0], errors['yule'][0])

    def test_run_reg(self):
        # Use data from https://www.coursera.org/learn/machine-learning
        features = get_ng_features()
        labels = get_ng_labels()
        reguls = (0., .001, .003, .01, .03, .1, .3, 1., 3., 10.)
        best_i = -1
        best_error = -1.
        for i in range(len(reguls)):
            err = get_ng_error(features, labels, reguls[i], 'xval')
            if best_i < 0 or err < best_error:
                best_i = i
                best_error = err
        self.assertAlmostEqual(reguls[best_i], 3., msg='not best lambda')
        # Ng gets a test error of 3.8599 but calculates it differently
        # Ridge regression from sklearn gives the expected result
        self.assertAlmostEqual(get_ng_error(features, labels, reguls[best_i], 'test').flatten()[0],
                7.14405231, msg='incorrect error on test data')

    def test_predict(self):
        self.addTypeEqualityFunc(np.ndarray, self.ndarr_almost_eq)
        features = np.array([
                [1., 0., 1.],
                [1., 0., .5],
                [1., 2., 0.],
                [1., 1., 0.],
                [1., 1., 1.]])
        model1 = np.array([0., 1., 2.])
        expected1 = np.array([2., 1., 2., 1., 3.])
        self.assertEqual(pn.learn.linreg.predict(features, model1), expected1,
                'incorrect predictions from weight vector')
        model2 = np.array([
                [0., 1.],
                [1., 2.],
                [2., 4.]])
        expected2 = np.array([
                [2., 5.],
                [1., 3.],
                [2., 5.],
                [1., 3.],
                [3., 7.]])
        self.assertEqual(pn.learn.linreg.predict(features, model2), expected2,
                'incorrect predictions from weight matrix')

def get_yule_data():
    data = adj_yule(load_yule())
    features = pd.DataFrame(data=data.values.copy(), 
            columns=['Constant', 'Out', 'Old', 'Pop'])
    features.iloc[:, 0] = 1.
    labels = pd.DataFrame(data=data.values[:, 0])
    return features, labels

def adj_yule(df):
    return df - 100.

def load_yule():
    path = os.path.dirname(os.path.realpath(__file__))
    infile = os.path.join(path, 'yule.data')
    data = pd.read_table(infile, sep=' ', index_col=False, header=None,
            names=['Paup', 'Out', 'Old', 'Pop'], dtype=np.float64)
    return data

def get_ng_error(features, labels, regul, key):
    model = pn.learn.linreg.run(features['train'], labels['train'], regularization=regul)
    predicted = pn.learn.linreg.predict(features[key], model)
    return pn.learn.mse(predicted, labels[key])

def get_ng_labels():
    files = {'train': 'y.data', 'xval': 'yval.data', 'test': 'ytest.data'}
    labels = {}
    for key in files:
        labels[key] = load_ng_data(files[key])
    return labels

def get_ng_features():
    degree = 8
    files = {'train': 'x.data', 'xval': 'xval.data', 'test': 'xtest.data'}
    features = {}
    for key in files:
        linfeat = load_ng_data(files[key])
        features[key] = get_polyfeat(linfeat, degree)
    # center and normalize
    _, means = pn.data.center(features['train'][:, 1:], out=features['train'][:, 1:])
    _, sd_adj = pn.data.normalize(features['train'][:, 1:], out=features['train'][:, 1:])
    for key in ('xval', 'test'):
        features[key][:, 1:] -= means
        features[key][:, 1:] *= 1. / sd_adj
    return features

def load_ng_data(fname):
    path = os.path.dirname(os.path.realpath(__file__))
    infile = os.path.join(path, fname)
    return np.loadtxt(infile)

def get_polyfeat(linfeat, degree):
    polyfeat = np.ones((linfeat.shape[0], degree + 1))
    for i in range(degree):
        polyfeat[:, i + 1] = polyfeat[:, i] * linfeat
    return polyfeat

if __name__ == '__main__':
    unittest.main()
