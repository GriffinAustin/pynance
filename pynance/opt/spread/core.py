"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Options - spreads (:mod:`pynance.opt.spread.core`)
==================================================

.. currentmodule:: pynance.opt.spread.core
"""

from __future__ import absolute_import

from .horiz import Horizontal

class Spread(object):
    """
    Wrapper class for :class:`pandas.DataFrame` for retrieving
    metrics on options spreads.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Options data.

    Attributes
    ----------
    data
    """
    def __init__(self, df):
        self.data = df

    def horiz(self):
        """
        Return a wrapper for accessing horizontal spreads.

        Returns
        -------
        out : :class:`pynance.opt.spread.horiz.Horizontal`
        """
        return Horizontal(self.data)
