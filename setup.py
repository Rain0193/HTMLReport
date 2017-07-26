#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


"""
===============================
HTMLReport
===============================
这个报告灵感来源于``HtmlTestRunner by tungwaiyip``.
Usage:
--------------
.. code-block:: python
    import unittest
    import HTMLReport
    
    
    # 测试套件
    suite = unittest.TestSuite()
    # 测试用例加载器
    loader = unittest.TestLoader()
    # 把测试用例加载到测试套件中
    suite.addTests(loader.loadTestsFromTestCase(TestStringMethods))
    
    # 测试用例执行器
    runner = HTMLReport.TestRunner(report_file_name='test',  # 报告文件名，默认“test”
                                   output_path='report',  # 保存文件夹名，默认“report”
                                   verbosity=2,  # 控制台输出详细程度，默认 2
                                   title='测试报告',  # 报告标题，默认“测试报告”
                                   description='无测试描述',  # 报告描述，默认“无测试描述”
                                   thread_count=2,  # 是否多线程测试（无序执行），默认 1
                                   sequential_execution=True  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   )
    # 执行测试用例套件
    runner.run(suite)
        
使用非常简单。

Links:
---------
* `Github <https://github.com/liushilive/HTMLReport>`_
"""

setup(
    name='HTMLReport',
    version='0.1.0',
    description="Python3 THML报告生成",
    long_description=__doc__,
    author="刘士",
    author_email='liushilive@outlook.com',
    url='https://github.com/liushilive/HTMLReport',
    packages=[
        'HTMLReport',
    ],
    package_dir={'HTMLReport':
                 'HTMLReport'},
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
