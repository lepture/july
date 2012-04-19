Quick Start
===========


Create a Project
----------------

You can easily create a project::

    july startproject PROJECT_NAME


This will create the folder structure of july project for you::

    PROJECT_NAME/
        setup.py
        PROJECT_NAME/
            __init__.py
            app.py
            static/
            templates/


Start a Server
--------------

::

    python app.py


Create an App
--------------

Just like `Create a Project`_ ::

    july startapp APP_NAME

This will create the folder structure of july app for you::

    APP_NAME/
        __init__.py
        handlers.py
        templates/
            APP_NAME/


Write an App
--------------

July App is like BluePrint in Flask, it splits a tornado project into
several apps.

The basic usage, consider your app as::

    myapp/
        __init__.py
        handlers.py

And in your ``~myapp.handlers`` define::

    class MyHandler(RequestHandler):
        def get(self):
            self.write('hello july app')

    handlers = [
        ('/', MyHandler),
    ]

    app = JulyApp('a readable name', __name__, handlers=handlers)

    # you may also add a handler by ``app.add_handler``
    # app.add_handler(('/', MyHandler))


the folder name for templates in your app, for example, in your app::

    myapp/
        __init__.py
        handlers.py
        templates/

so that template_folder is ``templates``. And you can define your app
with app template supports::

    app = JulyApp('name', __name__, template_folder='templates')


Register App to Project
-----------------------

July Application

This is a wrapper for ``tornado.web.Application``.
You define a JulyApplication::

    application = JulyApplication()

and when this application is called, it creates a
``tornado.web.Application``, which means, application() is somewhat a
``tornado.web.Application()``.

so, you can do more with application before it is called.

The most useful task for JulyApplication is registering a July App.
Define you July App, and register it to your application::

    simple_app = JulyApp('name', __name__, handlers=handlers)
    application.register_app(simple_app)

And start your application::

    application().listen(8888)
    ioloop.IOLoop.instance().start()
