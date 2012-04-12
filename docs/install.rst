Installation
============

The required library is Tornado_, and an optional library is SQLAlchemy_.
Although SQLAlchemy is optional, you should install it if you want a better solution
for database.

Tornado is a web server, and June Tornado is built on it. SQLAlchemy is a powerful database
engine, June Tornado provides an easy way to integrate it with Tornado.

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
    $ virtualenv ~/env/june

When the installation is finished, active this virtual environment::

    $ source ~/env/june/bin/active

Now, you are on a virtual environment called june. Any python package will be installed
on this june environment now::

    $ pip install junetornado
    $ pip install SQLAlchemy


System-Wide Installation
------------------------

This could be easy, if you are on Linux or Mac OS X::

    $ sudo pip install junetornado

if no pip available::

    $ sudo easy_install junetornado


Install from Source
--------------------

If you have git installed::

    $ git clone http://github.com/lepture/junetornado.git
    $ cd junetornado
    $ python setup.py install

