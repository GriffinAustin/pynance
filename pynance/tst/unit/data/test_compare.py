"""
Tests for performance comparison functions.

Copyright (c) 2016 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestCompare(unittest.TestCase):

    def test_compare(self):
        rng = pd.date_range('2016-03-28', periods=4)
        eqs = ('SCTY', 'SPWR')
        eq_dfs = [pd.DataFrame(index=rng, columns=['Close']) for i in range(len(eqs))]
        eq_dfs[0].iloc[:, 0] = [2., 4., 6., 8.]
        eq_dfs[1].iloc[:, 0] = [4., 4., 2., 6.]
        rel_perf = pn.data.compare(eq_dfs, eqs)
        self.assertTrue((rng == rel_perf.index).all(), 'incorrect index')
        self.assertTrue((list(eqs) == list(rel_perf)), 'incorrect column labels')
        self.assertTrue(np.allclose(np.array([[1., 2., 3., 4.], [1., 1., .5, 1.5]]).T, rel_perf.to_numpy()),
                'incorrect values')

if __name__ == '__main__':
    unittest.main()
