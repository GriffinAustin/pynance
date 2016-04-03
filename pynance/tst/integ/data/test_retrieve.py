"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Arka Dasgupta
@contact: arkadasgupta@gmail.com
@since: 2016-01-17
@summary: Integration Test for data retrieval from yahoo
"""

import datetime
import unittest

import pandas as pd

import pynance as pn


class TestRetrieve(unittest.TestCase):

    def test_equities(self):
        eqs = pn.data.equities()
        self.assertGreater(eqs.shape[0], 4000, 'too few equities found')
        self.assertEqual(eqs.shape[1], 2, 'wrong number of columns')
        self.assertTrue((eqs.columns == ['Security Name', 'Exchange']).all(),
                'incorrect column names')
        for eq in ('GE', 'MSFT',):
            self.assertTrue(eq in eqs.index, 'ticker {} not found'.format(eq))

    def test_pynance_data_get(self):
        self._init_get()
        pynance_data = pn.data.get('AAPL', '2014-03-03', '2014-03-07')
        self.assertEqual(pynance_data.shape, self.test_data_aapl.shape)
        for session, test_session in zip(pynance_data.values, self.test_data_aapl.values):
            # ignore adjusted close column in pandas data
            for value, test_value in zip(session[:-1], test_session):
                self.assertAlmostEqual(value, test_value)

    def test_pynance_data_get_with_default_end_date(self):
        self._init_get()
        current_date = datetime.datetime.today()
        past_date = current_date - datetime.timedelta(days=5)
        pynance_data = pn.data.get('GOOG', past_date.date().isoformat(), current_date.date().isoformat())
        pynance_data_default_end_date = pn.data.get('GOOG', past_date.date().isoformat())
        self.assertEqual(pynance_data.shape, pynance_data_default_end_date.shape)
        for session, default_session in zip(pynance_data.values, pynance_data_default_end_date.values):
            for value, test_value in zip(session, default_session):
                self.assertEqual(value, test_value)

    def _init_get(self):
        self.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
        self.index = pd.date_range('2014-03-03', periods=5)

        # Adjusted close values can change. So ignore them for tests
        self.test_data_aapl = pd.DataFrame([[5.23419991e+02, 5.30650009e+02, 5.22809990e+02, 5.27760010e+02,
                                             5.96953000e+07, 0],
                                            [5.30999977e+02, 5.32640015e+02, 5.27769997e+02, 5.31239983e+02,
                                             6.47850000e+07, 0],
                                            [5.30919975e+02, 5.34750023e+02, 5.29129974e+02, 5.32360008e+02,
                                             5.00157000e+07, 0],
                                            [5.32789978e+02, 5.34440002e+02, 5.28099991e+02, 5.30749985e+02,
                                             4.63722000e+07, 0],
                                            [5.31090019e+02, 5.31980026e+02, 5.26050011e+02, 5.30440018e+02,
                                             5.51824000e+07, 0]], self.index, self.columns)

if __name__ == '__main__':
    unittest.main()
