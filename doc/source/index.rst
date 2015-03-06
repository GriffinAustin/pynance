.. PyNance documentation master file, created by
   sphinx-quickstart on Mon Mar  2 23:08:30 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Examples:
   https://github.com/scipy/scipy/tree/master/doc/source
   https://raw.githubusercontent.com/scipy/scipy/master/doc/source/index.rst
   http://docs.scipy.org/doc/scipy/reference/

PyNance 
=======

:Release: |release|
:Date:  |today|

PyNance is open-source software with tools for retrieving, analysing and visualizing
data from stock and derivatives markets.

Installation
------------

For Python 2.7.x::

    pip install pynance

For Python 3.x.x::

    pip3 install pynance

Basics
---------------

Stock quotes maintained by `Yahoo! Finance <http://finance.yahoo.com/>`_ 
can be retrieved with the simple command::

    >>> import pynance as pn
    >>> ge = pn.data.get('ge', '1962', '2015')

Current options quotes can be retrieved using::

    >>> geopt, geexp, geeq = pn.opt.get('ge')

The options data retrieved can then be analysed using functions from :mod:`pynance.opt`.

Many of the functions in the submodules of :mod:`pynance.data` have been designed
for easy creation of features and labels for machine learning applications. You can
pass metrics from :mod:`pynance.tech` along with numeric parameters to create highly
customizable data sets to which machine learning algorithms can then be applied.
Examples can be found in the documentation for :mod:`pynance.data`.

Issues
------
PyNance is still in its early development stage. If you find a bug or think of a feature
you would like to see included in the next release,
please report the issue on 
`GitHub <https://github.com/aisthesis/pynance/issues>`_.

Reference
----------------

.. toctree::
   :maxdepth: 1

   chart
   common
   data
   interest
   opt
   pf
   tech

Index
-----

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
