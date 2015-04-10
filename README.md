PyNance
===
Lightweight Python library for assembling and analysing
financial data. Wraps Pandas and matplotlib for maximum
ease of use in accomplishing routine tasks in working with financial data.

Documentation
---
Detailed documentation at [PyNance website](http://pynance.net/).

Dependencies
---
Tested on:
* [Python](https://www.python.org/) 2.7.8, 3.4.2
* [matplotlib](http://matplotlib.org/index.html) 1.4.2, 1.4.3
* [NumPy](http://www.numpy.org/) 1.9.0, 1.9.2
* [Pandas](http://pandas.pydata.org/) 0.14.1, 0.15.1, 0.16.0
* [pandas-datareader](https://github.com/pydata/pandas-datareader) 0.1.1

PyNance will also work with other versions of Python
and Python packages. To verify that it works with yours,
simply run the unit tests for data retrieval, then try
making some charts with sample data you retrieve.

Additional dependencies for the `pynance.options` module:
* [lxml](http://lxml.de/) 3.4.2
* [html5lib](https://pypi.python.org/pypi/html5lib) 0.999
* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4/4.3.2) 4.3.2

Building the docs
---
To build the documentation using Sphinx outside of a virtual Python environment,
go to `./doc` and type `make html`. If you are using a virtual environment for any
dependencies, you will need to add `sphinx` and `numpydoc` to the virtual
environment before building the documentation. Explanation 
[here](http://stackoverflow.com/questions/4122040/how-to-make-sphinx-look-for-modules-in-virtualenv-while-building-html).
In other words, from within your virtual environment:

    $ pip install sphinx
    $ pip install numpydoc

Then build the documentation using `make html`.
