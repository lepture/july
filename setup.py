#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
kwargs = {}
major, minor = sys.version_info[:2]
if major >= 3:
    kwargs['use_2to3'] = True

import july
from setuptools import setup, find_packages

setup(
    name='july',
    version=july.__version__,
    author=july.__author__,
    author_email='lepture@me.com',
    url='http://project.lepture.com/july/',
    packages=find_packages(),
    description='July Tornado: a better way to organize your tornado project',
    long_description=july.__doc__,
    scripts=['scripts/july'],
    install_requires=[
        'tornado',
    ],
    include_package_data=True,
    license='BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    **kwargs
)
