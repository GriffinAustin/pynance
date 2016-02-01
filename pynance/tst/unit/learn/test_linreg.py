"""
Copyright (c) 2015-2016 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2016-01-28
@summary: Unit tests for linear regression
"""

import os
import sys
import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestData(unittest.TestCase):

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
        self.assertLessEqual(errors['ours'][0, 0], errors['yule'][0, 0])

    def test_run_reg(self):
        hitters_data = load_hitters()
        features = hitters_data[:, :-2]
        labels = hitters_data[:, -2]
        selector = np.array(hitters_data[:, -1] >= .5, dtype=bool)
        """
        print(features[:4, :])
        print(labels[:8])
        print(selector[:8])
        """
        reguls = [11498., 705., 50.]
        for i in range(len(reguls)):
            model = pn.learn.linreg.run(features, labels, regul=reguls[i])
            print('regularization parameter: {}'.format(reguls[i]))
            print(model)
            nonconst_coeffs = model[1:]
            print('sum of squares: {}'.format((nonconst_coeffs * nonconst_coeffs).sum()))

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

def load_hitters():
    path = os.path.dirname(os.path.realpath(__file__))
    infile = os.path.join(path, 'hitters.data')
    return np.loadtxt(infile)

if __name__ == '__main__':
    unittest.main()
