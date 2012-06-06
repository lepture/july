# -*- coding: utf-8 -*-

"""July

July is the best season for tornado, it provides a better way to
organize your tornado projects.

:license: BSD
:copyright: (c) 2012 - now, Hsiaoming Yang
"""

import os

#: always use utc time
os.environ['TZ'] = 'UTC'

#: always place python3 egg cache in /tmp
os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"


__version__ = '0.9.2'
__author__ = 'Hsiaoming Yang'
