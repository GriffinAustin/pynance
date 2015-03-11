"""
.. Copyright (c) 2014, 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Interest rates (:mod:`pynance.interest`)
========================================

.. currentmodule:: pynance.interest
"""

import datetime as dt
import math

import pandas as pd

def yrlygrowth(total_growth, years):
    """
    Determine the annual growth from the growth over an
    arbitrary time span.
    """
    return math.exp(math.log(total_growth) / years)

def yrlyret(total_interest, years):
    """
    Determine annual interest from interest compounded
    over an arbitrary time span.
    """
    return yrlygrowth(total_interest + 1.0, years) - 1.0

def growthfromrange(rangegrowth, startdate, enddate):
    """
    Annual growth given growth from start date to end date.
    """
    _yrs = (pd.Timestamp(enddate) - pd.Timestamp(startdate)).total_seconds() /\
            dt.timedelta(365.25).total_seconds()
    return yrlygrowth(rangegrowth, _yrs)

def retfromrange(rangeret, startdate, enddate):
    """
    Annual return given return from start date to end date.
    """
    return growthfromrange(1. + rangeret, startdate, enddate) - 1.

def growthtocont(annualgr):
    """
    Convert annual growth to continuous compounding rate
    """
    return math.log(annualgr)

def conttogrowth(contrate):
    """
    Convert continuous compounding rate to annual growth
    """
    return math.exp(contrate)

def compgrowth(annual_growth, years):
    """
    Compound `annual_growth` over given `years`.
    """
    return annual_growth**years

def compret(annual_interest, years):
    """
    Compound `annual_interest` over given `years`
    """
    return (1.0 + annual_interest)**years - 1.0

def pvannuity(rate, npmts, amt=1.):
    """
    Present value of `n` payments of a given size given
    an interest rate per payment interval of `rate`.

    .. versionchanged:: 0.3.0
       `amt` can be specified in function call.

    Parameters
    ----------
    rate : float
        Interest rate per payment period. Note that if
        payments are monthly and known interest rate is annual,
        `rate` must be calculated as effective *monthly* interest.
    npmts : int
        Number of payments.
    amt : float, optional
        Amount of each payment. Defaults to 1.
    """
    return amt * (1. - (1. + rate)**-npmts) / rate

def loanpayment(amount, rate, npmts):
    """
    Amount of a constant loan payment.

    Parameters
    ----------
    amount : float
        amount of loan
    rate : float
        interest rate for the given payment, i.e., monthly
        interest if the loan is to be paid off monthly.
    npmts : int
        number of payments to be made.

    Returns
    -------
    out : float
        amount to be paid each period.
    """
    return float(amount) / pvannuity(rate, npmts)
