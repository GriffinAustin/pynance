"""
For instructions on how to put a package on PyPI:
http://peterdowns.com/posts/first-time-with-pypi.html

To upload a new version to PyPI:
1. Udate `VERSION` below. 
2. Update version and release in `pynance/doc/source/conf.py`
3. Build documentation. Cf. instructions in `pynance/doc/Makefile`
4. Commit all changes. 
5. Create a tag for new version in git:
    % git tag 0.0.1 -m "Fixed some problems"
    % git tag -n # to verify that new tag is in list
    % git push --tags

6. Register and upload to PyPI Test:
% python setup.py register -r pypitest
% python setup.py sdist upload -r pypitest

7. Register and upload to PyPI Live:
% python setup.py register -r pypi
% python setup.py sdist upload -r pypi

8. Upload documentation to website.
"""

from setuptools import setup, find_packages

MAJOR   = 0
MINOR   = 5
MICRO   = 0
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        ]

KEYWORDS = [
        "finance",
        "investment",
        "stocks",
        "equities",
        "market",
        "options",
        "derivatives",
        ]

DEPENDENCIES = [
        "numpy",
        "pandas",
        "pandas-datareader>=0.1.1",
        "matplotlib"
        ]

TEST_DEPENDENCIES = [
        "nose",
        "pytz"
        ]
setup(
        name='pynance',
        packages=find_packages(),
        version=VERSION,
        description='Retrieve and analyse financial market data',
        author='Marshall Farrier',
        author_email='marshalldfarrier@gmail.com',
        url='http://pynance.net',
        download_url=('https://github.com/aisthesis/pynance/tarball/' + VERSION),
        keywords=' '.join(KEYWORDS),
        classifiers=CLASSIFIERS,
        install_requires=DEPENDENCIES,
        tests_require=TEST_DEPENDENCIES
        )
