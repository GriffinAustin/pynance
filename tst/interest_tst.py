"""
Unit tests for `interest` module

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import sys
import unittest

sys.path.append('../pynance')
import interest

class TestData(unittest.TestCase):

    def test_yrlygrowth(self):
        # growth of 8 over 3 years means annual growth of 2
        self.assertAlmostEqual(interest.yrlygrowth(8, 3), 2.0)

    def test_yrlyret(self):
        # interest of 2.0 over .5 yrs means growth of 3.0
        # so annual muliple of 9.0 and interest of 8.0
        self.assertAlmostEqual(interest.yrlyret(2, 0.5), 8.0)

    def test_compgrowth(self):
        # compound an annual growth of 16.0 over 0.5 yrs
        self.assertAlmostEqual(interest.compgrowth(16.0, 0.5), 4.0)

    def test_compret(self):
        # compound annual interest of 0.1 over 25 years
        self.assertAlmostEqual(interest.compret(0.1, 25), 9.83, places=2)

    def test_pvannuity(self):
        # 15% return for 5 years
        self.assertAlmostEqual(interest.pvannuity(0.15, 5), 3.352, places=3)

    def test_loanpayment(self):
        # 15% interest with 5 yrly payments for a loan of 1000
        self.assertAlmostEqual(interest.loanpayment(1000., 0.15, 5), 298.32, places=2)


if __name__ == '__main__':
    unittest.main()
