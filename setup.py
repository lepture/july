#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='july',
    version='1.0.1',
    author='Hsiaoming Young',
    author_email='lepture@me.com',
    url='http://lepture.com/project/july/',
    packages=['july', 'july.ext'],
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
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
