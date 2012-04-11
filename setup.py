#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='junetornado',
    version='0.1',
    author='Hsiaoming Young',
    author_email='lepture@me.com',
    url='http://lepture.com/project/june',
    packages=find_packages(),
    description='June Tornado: a better way to organize your tornado project',
    install_requires=[
        'tornado',
        'SQLAlchemy',
    ],
    include_package_data=True,
    license='BSD License',
)
