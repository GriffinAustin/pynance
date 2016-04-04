"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-02
@summary: Unit tests for data module
"""

from functools import partial
import unittest

import numpy as np
import pandas as pd

import pynance as pn

class TestLab(unittest.TestCase):

    def setUp(self):
        session_dates = [
                '2014-01-06',
                '2014-01-07',
                '2014-01-08',
                '2014-01-09',
                '2014-01-10',
                '2014-01-13',
                '2014-01-14',
                '2014-01-15',
                '2014-01-16',
                '2014-01-17']
        self.equity_data = pd.DataFrame(np.arange(1., 21.).reshape((10, 2)), index=session_dates,
                columns=['Volume', 'Adj Close'])
        self.equity_data.index.name = 'Date'

    def test_growth(self):
        prediction_interval = 2
        labels = pn.data.lab.growth(prediction_interval, 'Adj Close', self.equity_data)
        self.assertEqual(len(labels.index), len(self.equity_data.index) - prediction_interval)
        for i in range(len(labels.index)):
            self.assertAlmostEqual(labels.values[i], (i + 3.) / (i + 1.))

if __name__ == '__main__':
    unittest.main()
