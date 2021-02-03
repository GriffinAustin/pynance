PyNance
===
Lightweight Python library for assembling and analysing
financial data. Wraps `pandas` and `matplotlib` for maximum
ease of use. Included are tools for generating features
and labels for machine learning algorithms.

Dependencies
---
Tested on:
* [Python](https://www.python.org/) 3.9.1
* [matplotlib](http://matplotlib.org/index.html) 3.3.3
* [NumPy](http://www.numpy.org/) 1.19.5
* [Pandas](http://pandas.pydata.org/) 1.2.1
* [pandas-datareader](https://github.com/pydata/pandas-datareader) 0.9.0
* [mplfinance](https://github.com/matplotlib/mplfinance) 0.12.7a5

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

Development environment
---
To set up your virtual environment for development:

    $ mkvirtualenv -p /usr/local/bin/python pn-dev
    $ python setup.py develop

Release a new version
---
When branch `develop` has all desired substantive changes, it is
time to release the next version. This involves:

- create the new version and push it to Pypi
- reorganize the documentation in the `develop` branch

### Note on building the documentation
A note applying to both steps: The environment in which you
build the documentation must include the external dependencies
(`numpy`, `pandas`, etc.) mentioned above. Sphinx actually checks
for the presence of dependencies and will fail to build the
documentation if they are missing.

### Create the new version
Overview [here](http://peterdowns.com/posts/first-time-with-pypi.html).

In branch `develop` verify that all desired changes have been merged and that 
the documentation is up to date. Then:

1. Change the release version in `.setup.py` and in `./doc/source/conf.py` to the numbers desired for the
   version you are about to publish.
1. Build the documentation:

        $ cd ./doc
        $ make html
1. Merge to master.
1. Tag the release in GitHub.
1. Publish to PyPi.
1. Push the documentation to [pynance.net](http://pynance.net/):

Branches `develop` and `master` should now be the same. In preparation for the next
release (in the more distant future), you should now re-organize the 
documentation so that what was just committed
is archived and new documentation can be generated, as described in the following section.

### Reorganize the documentation
As example, let's say the version just committed is version `3.1.4`.

1. Move current *public* html to an archive directory:

        $ cd ./doc
        $ make archhtml ARCHDIR="3.1.4"
1. Add a link to version `3.1.4` in `./doc/source/index.rst` under 'Prior Versions'
1. Change version number in `./doc/source/conf.py` to `3.1.5`.
1. Rebuild current documentation:

        $ make html
1. Write new documentation to public directory:
    
        $ make pubhtml
1. Commit changes.

