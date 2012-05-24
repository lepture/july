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

July SQLAlchemy is converted from Flask-SQLAlchemy, all methods provided by
Flask-SQLAlchemy is available in July SQLAlchemy. But July provides more.

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
    options.sqlalchemy_engine = 'sqlite:////tmp/demo.sqlite'
    #: configure before importing database

    from july.database import db
    from models import User

    #: create a user
    user = User(username='lepture')
    db.session.add(user)
    db.session.commit()

    #: query a user
    user = db.session.query(User).filter(username='lepture').first()

    #: query a user
    user = User.query.filter(username='lepture').first()

    #: update a user
    user = User.query.filter(username='lepture').first()
    user.username = 'hsiaoming'
    db.session.add(user)
    db.session.commit()

    #: delete a user
    user = User.query.filter(username='lepture').first()
    db.session.delete(user)
    db.session.commit()


July database supports Django-like queries::

    User.query.filter_by(username__startswith='hsiao').order_by('-id')


Memcache
~~~~~~~~~~


Filter and Context
------------------


Message
--------

Good applications and user interfaces are all about feedback. For example,
when a user did some task, he wanted to know it worked or not.

