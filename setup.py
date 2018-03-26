#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import find_packages
from setuptools import setup

__author__ = "刘士"
__version__ = '1.1.6'

if sys.version_info < (3, 5):
    raise RuntimeError("The minimum support Python 3.5")

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: 没有找到pypandoc模块，无法将Markdown转换为RST")
    read_md = lambda f: open(f, 'r', encoding="utf-8").read()

setup(
    name='HTMLReport',
    version=__version__,
    description="Python3 Unittest HTML报告生成",
    # long_description=doc,
    long_description=read_md('README.md'),
    author=__author__,
    author_email='liushilive@outlook.com',
    url='https://github.com/liushilive/HTMLReport',
    packages=find_packages(),
    package_dir={'HTMLReport': 'HTMLReport'},
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='HtmlTestRunner TestRunner Html Reports',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests', install_requires=['pypandoc']
)
