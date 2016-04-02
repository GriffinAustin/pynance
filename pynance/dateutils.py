"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Dateutils (:mod:`pynance.dateutils`)
========================================

.. versionadded:: 0.5.0

.. currentmodule:: pynance.dateutils

Utility functions for working with dates.
"""

from pandas import Timestamp
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

def is_bday(date, bday=None):
    """
    Return true iff the given date is a business day.

    Parameters
    ----------
    date : :class:`pandas.Timestamp`
        Any value that can be converted to a pandas Timestamp--e.g.,
        '2012-05-01', dt.datetime(2012, 5, 1, 3)

    bday : :class:`pandas.tseries.offsets.CustomBusinessDay`
        Defaults to `CustomBusinessDay(calendar=USFederalHolidayCalendar())`.
        Pass this parameter in performance-sensitive contexts, such
        as when calling this function in a loop. The creation of the `CustomBusinessDay`
        object is the performance bottleneck of this function.
        Cf. `pandas.tseries.offsets.CustomBusinessDay
        <http://pandas.pydata.org/pandas-docs/stable/timeseries.html#custom-business-days-experimental>`_.

    Returns
    -------
    val : bool
        True iff `date` is a business day
    """
    _date = Timestamp(date)
    if bday is None:
        bday = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    return _date == (_date + bday) - bday

