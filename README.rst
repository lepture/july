July
=====

.. image:: https://secure.travis-ci.org/lepture/july.png
    :target: https://secure.travis-ci.org/lepture/july


July is the best season for Tornado , it’s all about how to organize a tornado
project. It is inspired by Django and Flask.

    This is a project by `Hsiaoming Yang <http://lepture.com>`_.
    All projects are listed at `project page <http://project.lepture.com>`_.

- `Documentation <http://july.readthedocs.org/>`_
- `GitHub <https://github.com/lepture/july>`_
- `PyPi <http://pypi.python.org/pypi/july>`_

Feature
--------

- Organize tornado as App
- Built-in SQLAlchemy
- Flash message design
- Built-in Mail App

and more.

Overview
---------

A minimal July Application::

    from july.web import JulyHandler
    from july.app import JulyApplication


    class HelloHandler(JulyHandler):
        def get(self):
            self.write('Hello July')

        handlers = [('/', HelloHandler)]
        application = JulyApplication(handlers=handlers)

        if __name__ == '__main__':
        from july import run_server
        run_server(application)

Get more information on `Documentation`_.

Installation
--------------

This project is **UNDER DEVELOPMENT**, it is not robust.

- Install with pip::

    $ pip install july

- Install with easy_install::

    $ easy_install july

Bug report
-----------

If you have any trouble, report bug at `GitHub Issue <https://github.com/lepture/july/issues>`_.
