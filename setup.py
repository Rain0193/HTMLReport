#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 5):
    raise RuntimeError("The minimum support Python 3.5")

from setuptools import find_packages
from setuptools import setup

from HTMLReport import __version__, __author__

try:
    from pypandoc import convert

    read_md = convert('README.md', 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = open('README.md', 'r', encoding="utf-8").read()

setup(
    name='HTMLReport',
    version=__version__,
    description="Python3 Unittest HTML报告生成器",
    long_description=read_md,
    author=__author__,
    author_email='liushilive@outlook.com',
    url='https://github.com/liushilive/HTMLReport',
    project_urls={
        'The report template': 'https://liushilive.github.io/report/report/#en',
        '报告样板': 'https://liushilive.github.io/report/report/#cn'
    },
    packages=find_packages(),
    package_dir={'HTMLReport': 'HTMLReport'},
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='HtmlTestRunner test runner html reports unittest',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests'
)
