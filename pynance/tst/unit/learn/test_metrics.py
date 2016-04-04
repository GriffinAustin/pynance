"""
Copyright (c) 2016 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2016-02-01
@summary: Unit tests for machine learning metrics
"""

import unittest

import numpy as np

import pynance as pn

class TestMetrics(unittest.TestCase):

    def ndarr_almost_eq(self, a, b, msg=None):
        if not np.allclose(a, b):
            print('ndarrays not equal:')
            print(a)
            print(b)
            raise self.failureException(msg)

    def test_mse_vector(self):
        actual = np.array([1., 2., 3.])
        predicted = np.array([2., 4., 2.])
        self.assertAlmostEqual(pn.learn.mse(predicted, actual), 2.)

    def test_mse_matrix(self):
        self.addTypeEqualityFunc(np.ndarray, self.ndarr_almost_eq)
        actual = np.array([
                [1., 3.],
                [2., 1.],
                [3., 2.]])
        predicted = np.array([
                [2., 1.],
                [4., -1.],
                [2., 3.]])
        self.assertEqual(pn.learn.mse(predicted, actual), np.array([2., 3.]))

    def test_stderr_vector(self):
        actual = np.array([-1., 0., 1.])
        predicted = np.array([1., 2., -1.])
        self.assertAlmostEqual(pn.learn.stderr(predicted, actual), 2.)

    def test_stderr_matrix(self):
        self.addTypeEqualityFunc(np.ndarray, self.ndarr_almost_eq)
        actual = np.array([
                [1., -1.],
                [2., 0.],
                [3., 1.]])
        predicted = np.array([
                [2., 1.],
                [1., 2.],
                [2., -1.]])
        self.assertEqual(pn.learn.stderr(predicted, actual), np.array([1., 2.]))

if __name__ == '__main__':
    unittest.main()
