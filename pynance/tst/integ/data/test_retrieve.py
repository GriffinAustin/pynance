"""
Copyright (c) 2021 Griffin Austin
license http://opensource.org/licenses/MIT

@author: Griffin Austin
@contact: griffinaustin@protonmail.com
@since: 2020-01-25
@summary: Integration Test for data retrieval from Stooq
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
                self.assertAlmostEqual(value, test_value, places=3)

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
        self.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.index = pd.date_range('2014-03-03', periods=5)

        # Adjusted close values can change. So ignore them for tests
        self.test_data_aapl = pd.DataFrame([[17.043, 17.053, 16.862, 17.003, 246767076],
                                            [17.078, 17.130, 16.928, 17.013, 206740872],
                                            [17.018, 17.140, 16.961, 17.065, 223028444],
                                            [17.021, 17.073, 16.917, 17.029, 288981388],
                                            [16.764, 17.010, 16.759, 16.917, 266327067]], self.index, self.columns)

if __name__ == '__main__':
    unittest.main()
