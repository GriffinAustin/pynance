"""
.. Copyright (c) 2015, 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Machine learning (:mod:`pynance.learn`)
=======================================

.. currentmodule:: pynance.learn

:mod:`pynance.learn.linreg`

:mod:`pynance.learn.metrics`
"""

from __future__ import division, absolute_import, print_function

__all__ = ["linreg", "metrics"]

from . import linreg
from . import metrics
from .metrics import *
