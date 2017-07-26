from setuptools import setup


setup(
    name='HTMLReport',
    version='0.0.4',
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
    keywords='Html Reports',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests'
)
