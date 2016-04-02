"""
Copyright (c) 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import unittest

import pynance as pn

class TestCovCall(unittest.TestCase):

    def setUp(self):
        # from McMillan, pp. 44f.
        self.args = (43, 3, 45, 500, 40, 15, 1)

    def test_get(self):
        df = pn.opt.covcall.get(*self.args)
        self.assertAlmostEqual(df.loc['Eq Cost', 'Value'], 21500.)
        self.assertAlmostEqual(df.loc['Option Premium', 'Value'], 1500.)
        self.assertAlmostEqual(df.loc['Commission', 'Value'], 40.)
        self.assertAlmostEqual(df.loc['Total Invested', 'Value'], 20040.)
        self.assertAlmostEqual(df.loc['Dividends', 'Value'], 500.)
        self.assertAlmostEqual(df.loc['Eq if Ex', 'Value'], 22500.)
        self.assertAlmostEqual(df.loc['Comm if Ex', 'Value'], 15.)
        self.assertAlmostEqual(df.loc['Profit if Ex', 'Value'], 2945.)
        self.assertAlmostEqual(df.loc['Ret if Ex', 'Value'], .147)
        self.assertAlmostEqual(df.loc['Profit if Unch', 'Value'], 1960.)
        self.assertAlmostEqual(df.loc['Ret if Unch', 'Value'], .098, places=3)
        self.assertAlmostEqual(df.loc['Break_Even Price', 'Value'], 39.08)
        self.assertAlmostEqual(df.loc['Protection Pts', 'Value'], 3.92)
        self.assertAlmostEqual(df.loc['Protection Pct', 'Value'], .091, places=3)

if __name__ == '__main__':
    unittest.main()
