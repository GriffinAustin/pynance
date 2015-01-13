"""
Calculations involving compounded interest.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import math

def get_growth(total_growth, years):
    """
    Determine the annual growth from the growth over an
    arbitrary time span.
    """
    return math.exp(math.log(total_growth) / years)

def get_interest(total_interest, years):
    """
    Determine annual interest from interest compounded
    over an arbitrary time span.
    """
    return get_growth(total_interest + 1.0, years) - 1.0

def get_compounded_growth(annual_growth, years):
    """
    Compound `annual_growth` over given `years`.
    """
    return annual_growth**years

def get_compounded_interest(annual_interest, years):
    """
    Compound `annual_interest` over given `years`
    """
    return (1.0 + annual_interest)**years - 1.0
