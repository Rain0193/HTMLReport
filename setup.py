#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages

from HTMLReport.HTMLReport import __version__, __author__

doc = """
HTMLReport
==========

``HTMLReport``\ 是一个单元测试测试运行器，可以将测试结果保存在Html文件中，用于人性化的结果显示。仅支持\ **Python
3.x**

    多线程不支持 @classmethod 装饰器！采用单线程模式工作！

安装
====

要安装HTMLReport，请在终端中运行此命令

.. code:: py

    $ pip install HTMLReport

这是安装HTMLReport的首选方法，因为它将始终安装最新的稳定版本。如果您没有安装\ `pip <https://pip.pypa.io/>`__\ ，则该\ `Python安装指南 <http://docs.python-guide.org/en/latest/starting/installation/>`__\ 可以指导您完成该过程。

使用方法
========

.. code:: py

    import unittest
    import HTMLReport


    # 测试套件
    suite = unittest.TestSuite()
    # 测试用例加载器
    loader = unittest.TestLoader()
    # 把测试用例加载到测试套件中
    suite.addTests(loader.loadTestsFromTestCase(TestStringMethods))

    # 测试用例执行器
    runner = HTMLReport.TestRunner(report_file_name='test',  # 报告文件名，默认“test+时间戳”
                                   output_path='report',  # 保存文件夹名，默认“report”
                                   title='一个简单的测试报告',  # 报告标题，默认“测试报告”
                                   description='随意描述',  # 报告描述，默认“无测试描述”
                                   thread_count=10,  # 并发线程数量（无序执行测试），默认数量 1
                                   sequential_execution=True  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   )
    # 执行测试用例套件
    runner.run(suite)

Links:
------

-  https://github.com/liushilive/HTMLReport
"""

if sys.version_info < (3, 5):
    raise RuntimeError('本模块最低支持 Python 3.5')

setup(
    name='HTMLReport',
    version=__version__,
    description="Python3 Unittest HTML报告生成",
    long_description=doc,
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
    test_suite='tests'
)
