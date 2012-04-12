#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from junetornado import __version__

setup(
    name='junetornado',
    version=__version__,
    author='Hsiaoming Young',
    author_email='lepture@me.com',
    url='http://lepture.com/project/june',
    packages=['junetornado', 'junetornado.ext'],
    description='June Tornado: a better way to organize your tornado project',
    scripts=['scripts/june.admin'],
    install_requires=[
        'tornado',
        'SQLAlchemy',
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
