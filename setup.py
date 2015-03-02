"""
For instructions on how to put a package on PyPI:
http://peterdowns.com/posts/first-time-with-pypi.html

To upload a new version to PyPI:
1. Udate `VERSION` below. 
2. Commit all changes. 
3. Create a tag for new version in git:
    % git tag 0.0.1 -m "Fixed some problems"
    % git tag # to verify that new tag is in list
    % git push --tags

4. Register and upload to PyPI Test:
% python setup.py register -r pypitest
% python setup.py sdist upload -r pypitest

5. Register and upload to PyPI Live:
% python setup.py register -r pypi
% python setup.py sdist upload -r pypi
"""

from setuptools import setup, find_packages

MAJOR   = 0
MINOR   = 1
MICRO   = 2
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

CLASSIFIERS = [
        "Development Status :: 3 - Alpha",
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
        "matplotlib",
        "lxml",
        "html5lib",
        "beautifulsoup4",
        ]

setup(
        name='pynance',
        packages=find_packages(),
        version=VERSION,
        description='Retrieve and analyse financial market data',
        author='Marshall Farrier',
        author_email='marshalldfarrier@gmail.com',
        url='https://github.com/aisthesis/pynance',
        download_url=('https://github.com/aisthesis/pynance/tarball/' + VERSION),
        keywords=' '.join(KEYWORDS),
        classifiers=CLASSIFIERS,
        install_requires=DEPENDENCIES
        )
