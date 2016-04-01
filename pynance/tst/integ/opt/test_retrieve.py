"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Arka Dasgupta
@contact: arkadasgupta@gmail.com
@since: 2016-01-17
@summary: Integration Test for data retrieval from yahoo
"""

import unittest

import pynance as pn


class TestRetrieve(unittest.TestCase):

    def test_get(self):
        opts = pn.opt.get('ge')
        self.assertGreaterEqual(opts.data.shape[1], 4, 'at least 4 columns of options data retrieved')
        self.assertGreaterEqual(opts.data.shape[0], 1, 'at least 1 row of options data retrieved')

if __name__ == '__main__':
    unittest.main()
