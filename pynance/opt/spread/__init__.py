"""
.. Copyright (c) 2014- Marshall Farrier
   license http://opensource.org/licenses/MIT

Options spreads (:mod:`pynance.opt.spread`)
===============================================

.. currentmodule:: pynance.opt.spread

:mod:`pynance.opt.spread.core`

:mod:`pynance.opt.spread.diag`

:mod:`pynance.opt.spread.horiz`

:mod:`pynance.opt.spread.multi`

:mod:`pynance.opt.spread.vert`
"""
from __future__ import absolute_import

__all__ = ["diag", "core"]

# imported directly into module
from . import core
from .core import *

# imported as submodule
#from . import diag
