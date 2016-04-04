"""
Copyright (c) 2016 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2016-03-31
@summary: Unit tests for dateutils module
"""

import datetime as dt
import unittest

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

import pynance as pn

class TestDateUtils(unittest.TestCase):

    def setUp(self):
        self.bday = CustomBusinessDay(calendar=USFederalHolidayCalendar())

    def test_is_bday(self):
        self.assertTrue(pn.dateutils.is_bday('2016-03-31'), 'weekday input as text')
        self.assertTrue(pn.dateutils.is_bday(dt.datetime(2016, 3, 11, 4, 23, 7), bday=self.bday), 
                'weekday before DST input as datetime with hours, minutes, seconds')
        self.assertTrue(pn.dateutils.is_bday(dt.datetime(2015, 12, 24), bday=self.bday), 
                'Christmas Eve on Thursday')
        self.assertFalse(pn.dateutils.is_bday('2015-12-25', bday=self.bday), 'Christmas on Friday')
        self.assertFalse(pn.dateutils.is_bday('2015-07-03', bday=self.bday), 'July 3 on Friday')
        self.assertFalse(pn.dateutils.is_bday(dt.datetime(2016, 4, 2), bday=self.bday), 'Saturday')
        self.assertFalse(pn.dateutils.is_bday(dt.datetime(2014, 1, 20), bday=self.bday), 'MLK day')

if __name__ == '__main__':
    unittest.main()
