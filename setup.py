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

from distutils.core import setup

VERSION = '0.1.0'

CLASSIFIERS = [
        "Development Status :: 4 - Beta",
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

setup(
        name='pynance',
        packages=['pynance'],
        version=VERSION,
        description='Library for retrieving and analysing financial data',
        author='Marshall Farrier',
        author_email='marshalldfarrier@gmail.com',
        url='https://github.com/aisthesis/pynance',
        download_url='https://github.com/aisthesis/pynance/tarball/0.1',
        keywords=['finance'],
        classifiers=CLASSIFIERS,
        )
