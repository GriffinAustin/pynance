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

PyNance is open-source software for retrieving, analysing and visualizing
data from stock and derivatives markets. It includes tools for generating
features and labels for machine learning algorithms.

Installation
------------
PyNance depends on several powerful libraries that can be tricky to install, specifically
`NumPy <http://www.numpy.org/>`_, `Pandas <http://pandas.pydata.org/>`_, and `matplotlib
<http://matplotlib.org/index.html>`_. Unless you have already installed these libraries,
it is recommended to install the following individually using `pip`, as you will likely need to 
debug one or more of these installations::

    pip install matplotlib
    pip install numpy
    pip install pandas
    pip install pandas-datareader
    pip install pynance

Or for Python 3.x.x use `pip3` instead of `pip`.

If you already have at least NumPy, Pandas and matplotlib installed or just prefer
installing in one big step::

    pip install pynance

Basics
---------------

Stock quotes maintained by `Yahoo! Finance <http://finance.yahoo.com/>`_ 
can be retrieved with the simple command::

    >>> import pynance as pn
    >>> ge = pn.data.get('ge', '1962', '2015')

Current options quotes can be retrieved using::

    >>> geopt, geexp = pn.opt.get('ge').info()

The options data retrieved can then be analysed using functions from :mod:`pynance.opt`.

Many of the functions in the submodules of :mod:`pynance.data` have been designed
for easy creation of features and labels for machine learning applications. You can
pass metrics from :mod:`pynance.tech` along with numeric parameters to create highly
customizable data sets to which machine learning algorithms can then be applied.
Examples can be found in the documentation for :mod:`pynance.data`.

Issues
------
Please help us by reporting any problems you find and sharing your ideas for new features.

If you find a bug or think of a feature
you would like to see included in the next release,
please report the issue on 
`GitHub <https://github.com/aisthesis/pynance/issues>`_ in accordance with
the `Scipy guidelines <http://scipy.org/bug-report.html#guidelines-for-submitting-bugs>`_.

Reference
----------------

.. toctree::

   chart
   common
   data
   dateutils
   interest
   learn
   opt
   pf
   tech

Index
-----

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Prior Versions
--------------
* `0.2.0 <0.2.0/index.html>`_
* `0.3.0 <0.3.0/index.html>`_
* `0.3.1 <0.3.1/index.html>`_
* `0.4.0 <0.4.0/index.html>`_
