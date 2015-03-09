"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - diagonal spreads (:mod:`pynance.opt.spread.diag`)
==================================================

.. currentmodule:: pynance.opt.spread.diag
"""

from __future__ import absolute_import

import numpy as np
import pandas as pd

from . import price

class Diagonal(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on diagonal spreads

    Objects of this class are not intended for direct instantiation
    but are created as attributes of objects of type 
    :class:`pynance.opt.spread.core.Spread`.

    .. versionadded:: 0.3.0

    Parameters
    ----------
    df: :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data
    """
    def __init__(self, df):
        self.data = df
