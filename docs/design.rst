Design Pattern
================

Configuration
----------------

.. _project-vs-app:

Project vs App
---------------

.. _database-and-cache:

Database and Cache
------------------

For production project, database is a must, and cache will improve the performance.
But writting raw sql can be very tough, and in most cases, you would like an ORM
instead of raw sql.

There are many ORM engines, but July chooses SQLAlchemy_ . This section will not
cover every piece of SQLAlchemy, instead, you should head over to SQLAlchemy
official site for more documentation.

SQLAlchemy
~~~~~~~~~~~~

Install SQLAlchemy::

    pip install sqlalchemy


In your July project, initialize sqlalchemy options before import database::

    # models.py
    from july.database import db
    from sqlalchemy import Column, Integer, String

    class User(db.Model):
        id = Column(Integer, primary_key=True)
        username = Column(String(30))


    # app.py
    from tornado.options import options
    options.sqlalchemy_master = 'sqlite:////tmp/demo.sqlite'
    #: configure before importing database

    from july.database import db
    from models import User

    #: create a user
    user = User(username='lepture')
    db.master.add(user)
    db.master.commit()

    #: query a user
    user = db.master.query(User).filter(username='lepture').first()

    #: query a user
    user = User.query.filter(username='lepture').first()

    #: update a user
    user = User.query.filter(username='lepture').first()
    user.username = 'hsiaoming'
    db.master.add(user)
    db.master.commit()

    #: delete a user
    user = User.query.filter(username='lepture').first()
    db.master.delete(user)
    db.master.commit()

July database supports master-slave database, when you initialize like::

    from tornado.options import options
    options.sqlalchemy_master = 'mysql://user:pass@host:3306/db?charset=utf8'
    options.sqlalchemy_slaves = {
        'db1': 'mysql://user:pass@host1:3306/db?charset=utf8',
        'db2': 'mysql://user:pass@host2:3306/db?charset=utf8',
    }
    #: remember set pool recycle when using mysql
    options.sqlalchemy_kwargs = {"pool_recycle": 3600}

    #: now you can get data from slave database
    db.slave('db1').query(User).filter_by(username='lepture').first()

    #: other syntax available
    User.slave('db1').filter_by(username='lepture').first()

    #: not specify a key
    User.slave().filter_by(username='lepture').first()


July database supports Django-like queries::

    User.query.filter_by(username__startswith='hsiao').order_by('-id')


Memcache
~~~~~~~~~~


Filter and Context
------------------


Message
--------
