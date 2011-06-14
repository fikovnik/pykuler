#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from pkg_resources import resource_filename

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup (
    name = "pykuler",
    version = "1.2",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    install_requires = ['BeautifulSoup'],
    author = "Filip Krikava",
    author_email = "krikava@gmail.com",
    description = "Unofficial Python API for Adobe Kuler.",
    long_description = read("README.md"),
    license = "http://www.opensource.org/licenses/mit-license.php",
    keywords = "colors kuler adobe",
    url = "https://github.com/fikovnik/pykuler",
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
    ],
    test_suite = 'test',
    zip_safe = True,
)
