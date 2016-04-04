"""
Tests for portfolio optimization functions.

Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import unittest

import numpy as np

import pynance as pn

class TestPf(unittest.TestCase):

    def test_optimize(self):
        # Capinski, Zastawniak, pp. 76f.
        exp_rets = np.array([.1, .15, .2])
        covs = np.array([
            [.0784, -.0067, .0175],
            [-.0067, .0576, .0120],
            [.0175, .0120, .0625]])
        a, b, least_risk_ret = pn.pf.optimize(exp_rets, covs)
        _a_exp = np.array([-8.614, -2.769, 11.384])
        _b_exp = np.array([1.578, .845, -1.422])
        _ret_exp = .146
        for i in range(3):
            self.assertAlmostEqual(a[i], _a_exp[i], places=2)
            self.assertAlmostEqual(b[i], _b_exp[i], places=2)
        self.assertAlmostEqual(least_risk_ret, _ret_exp, places=3)

if __name__ == '__main__':
    unittest.main()
