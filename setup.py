#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from july import __version__, __author__

setup(
    name='july',
    version=__version__,
    author=__author__,
    author_email='lepture@me.com',
    url='http://lepture.com/project/july/',
    packages=find_packages(),
    description='July Tornado: a better way to organize your tornado project',
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
)
