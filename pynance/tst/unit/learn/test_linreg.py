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
        model = pn.learn.linreg.run(features, labels)
        expected_model = [12.88, .75, .06, -.31]
        for actual, expected in zip(model, expected_model):
            self.assertAlmostEqual(actual, expected, places=2)

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
    infile = os.path.join(path, 'yule.dat')
    data = pd.read_table(infile, sep=' ', index_col=False, header=None,
            names=['Paup', 'Out', 'Old', 'Pop'], dtype=np.float64)
    return data

if __name__ == '__main__':
    unittest.main()
