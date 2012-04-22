.. _installation:

Installation
============

The required library is Tornado_, and optional libraries are SQLAlchemy_ and memcache.

You don't need SQLAlchemy and memcache right now, but you will find that they are pretty
useful, in that case, you could head over to :ref:`database-and-cache` for detail
information.

Tornado is a web server, and July is built on it.
July provides an better way to organize your tornado project.

.. _Tornado: http://tornadoweb.org
.. _SQLAlchemy: http://www.sqlalchemy.org


virtualenv
----------

Virtualenv is probably what you want to use during development,
and if you have shell access to your production machines,
you’ll probably want to use it there, too.

It is strongly suggested that you develop on virtualenv.

If you are on Linux or Mac OS X, you can install it with::

    $ sudo pip install virtualenv

if you have no pip::

    $ sudo easy_install virtualenv

And you should use **pip** instead of easy_install, install pip with::

    $ sudo easy_install pip

If you are on Windows, you should try **MinGW** or **Cygwin** .

Read document of virtualenv for a better life. But you can start now with::

    $ mkdir ~/env
    $ virtualenv ~/env/july

When the installation is finished, active this virtual environment::

    $ source ~/env/july/bin/active

Now, you are on a virtual environment called july. Any python package will be installed
on this july environment now::

    $ pip install july


System-Wide Installation
------------------------

This could be easy, if you are on Linux or Mac OS X::

    $ sudo pip install july

if no pip available::

    $ sudo easy_install july


Install from Source
--------------------

If you have git installed::

    $ git clone http://github.com/lepture/july.git
    $ cd july
    $ python setup.py install

