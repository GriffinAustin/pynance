"""
Calculations involving compounded interest.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import math

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

def pvannuity(ret, n):
    """
    Present value of n constant payments assuming
    an interest rate per payment interval of `ret`
    """
    return (1. - (1. + ret)**-n) / ret

def loanpayment(amount, rate, n_payments):
    """
    Return amount of a constant loan payment

    Parameters
    ---
    amount : float
        amount of loan

    rate : float
        interest rate for the given payment, i.e., monthly
        interest if the loand is to be paid off monthly

    n_payments : int
        number of payments to be made

    Returns
    --
    out : float
        amount to be paid each period
    """
    return float(amount) / pvannuity(rate, n_payments)

