"""
Unit tests for `interest` module

Copyright (c) 2014, 2015 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import sys
import unittest

import pynance as pn

class TestInterest(unittest.TestCase):

    def test_yrlygrowth(self):
        # growth of 8 over 3 years means annual growth of 2
        self.assertAlmostEqual(pn.interest.yrlygrowth(8, 3), 2.0)

    def test_yrlyret(self):
        # interest of 2.0 over .5 yrs means growth of 3.0
        # so annual muliple of 9.0 and interest of 8.0
        self.assertAlmostEqual(pn.interest.yrlyret(2, 0.5), 8.0)

    def test_compgrowth(self):
        # compound an annual growth of 16.0 over 0.5 yrs
        self.assertAlmostEqual(pn.interest.compgrowth(16.0, 0.5), 4.0)

    def test_compret(self):
        # compound annual interest of 0.1 over 25 years
        self.assertAlmostEqual(pn.interest.compret(0.1, 25), 9.83, places=2)

    def test_pvannuity(self):
        # 15% return for 5 years
        self.assertAlmostEqual(pn.interest.pvannuity(0.15, 5), 3.352, places=3)
        # 10 payments of 10k at 18%
        self.assertAlmostEqual(pn.interest.pvannuity(.18, 10, 10000.), 44941., places=0)

    def test_loanpayment(self):
        # 15% interest with 5 yrly payments for a loan of 1000
        self.assertAlmostEqual(pn.interest.loanpayment(1000., 0.15, 5), 298.32, places=2)

    def test_growthfromrange(self):
        # 15% return from 2014-01-12 to 2015-06-30
        self.assertAlmostEqual(pn.interest.growthfromrange(1.15, '2014-01-12', '2015-06-30'),
                1.100314)

    def test_retfromrange(self):
        # 15% return from 1999-12-01 to 2000-03-15
        self.assertAlmostEqual(pn.interest.retfromrange(.15, '1999-12-01', '2000-03-15'),
                .626079, places=6)

    def test_growthtocont(self):
        # 10% annual return
        self.assertAlmostEqual(pn.interest.growthtocont(1.1), .0953102)

    def test_conttogrowth(self):
        # 10% continuous
        self.assertAlmostEqual(pn.interest.conttogrowth(.1), 1.1051709)


if __name__ == '__main__':
    unittest.main()
