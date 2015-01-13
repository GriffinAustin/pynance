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

    def test_get_multiple(self):
        # multiple of 8 over 3 years means annual multiple of 2
        self.assertAlmostEqual(interest.get_multiple(8, 3), 2.0)

    def test_get_interest(self):
        # interest of 2.0 over .5 yrs means multiple of 3.0
        # so annual muliple of 9.0 and interest of 8.0
        self.assertAlmostEqual(interest.get_interest(2, 0.5), 8.0)

    def test_get_compounded_multiple(self):
        # compound an annual multiple of 16.0 over 0.5 yrs
        self.assertAlmostEqual(interest.get_compounded_multiple(16.0, 0.5), 4.0)

    def test_get_compounded_interest(self):
        # compound annual interest of 0.1 over 25 years
        self.assertAlmostEqual(interest.get_compounded_interest(0.1, 25), 9.83, places=2)


if __name__ == '__main__':
    unittest.main()
