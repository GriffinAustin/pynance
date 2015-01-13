"""
Calculations involving compounded interest.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import math

def get_multiple(total_multiple, years):
    """
    Determine the annual multiple from the multiple over an
    arbitrary time span.
    """
    return math.exp(math.log(total_multiple) / years)

def get_interest(total_interest, years):
    """
    Determine annual interest from interest compounded
    over an arbitrary time span.
    """
    return get_multiple(total_interest + 1.0, years) - 1.0

def get_compounded_multiple(annual_multiple, years):
    """
    Compound `annual_multiple` over given `years`.
    """
    return annual_multiple**years

def get_compounded_interest(annual_interest, years):
    """
    Compound `annual_interest` over given `years`
    """
    return (1.0 + annual_interest)**years - 1.0
