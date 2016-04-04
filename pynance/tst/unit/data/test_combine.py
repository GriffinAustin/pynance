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

class TestCombine(unittest.TestCase):

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

    def test_labeledfeatures(self):
        _n_featsess = 2
        _ave_int = 3
        _pred_int = 1
        _featfuncs = []
        # growth and relative volume functions
        _featfuncs.append(pn.decorate(partial(pn.tech.growth, selection='Adj Close'), title='G'))
        _featfuncs.append(pn.decorate(partial(pn.tech.ratio_to_ave, _ave_int), title='V'))
        _featfunc = pn.decorate(partial(pn.data.feat.fromfuncs, _featfuncs, _n_featsess, skipatstart=_ave_int),
                _ave_int + _n_featsess - 1)
        _labfunc = pn.decorate(partial(pn.data.lab.growth, _pred_int, 'Adj Close'), _pred_int)
        features, labels = pn.data.labeledfeatures(self.equity_data, _featfunc, _labfunc)
        self.assertEqual(features.values.shape[0], labels.values.shape[0])
        self.assertEqual(features.values.shape[1], 5)
        for i in range(1, len(features.index)):
            self.assertAlmostEqual(features.loc[:, '-1 G'].values[i], 
                    features.loc[:, '0 G'].values[i - 1])
            self.assertAlmostEqual(features.loc[:, '-1 V'].values[i], 
                    features.loc[:, '0 V'].values[i - 1])
        for i in range(5):
            self.assertAlmostEqual(features.loc[:, '0 G'].values[i], (i + 5.) / (i + 4.))
            self.assertAlmostEqual(features.loc[:, '0 V'].values[i], (2. * i + 9.) / (2. * i + 5.))
            self.assertAlmostEqual(labels.values[i], (i + 6.) / (i + 5.))

if __name__ == '__main__':
    unittest.main()
