.. _quickstart:

Quickstart
===========

This section assumes you already have July installed. If you do not,
head over to the :ref:`installation` section.


A Minimal Application
----------------------

A minimal July application looks something like this::

    from july import JulyHandler, JulyApplication


    class HelloHandler(JulyHandler):
        def get(self):
            self.write('Hello July')

    handlers = [('/', HelloHandler)]
    application = JulyApplication(handlers=handlers)

    if __name__ == '__main__':
        from july import run_server
        run_server(application)

Just save it as `hello.py` (or any name you like) and run it with your Python
interpreter::

    $ python hello.py

Now browser at `127.0.0.1:8000 <http://127.0.0.1:8000>`_ , and you should see
a "Hello July" greeting.

To stop the server, hit Ctrl-C.

So how did it work?

1. Server: we created a server by ``july.run_server``, it listens on port 8000,
   any request to this port (8000) will be handled by the server's application.
   The server itself does nothing, the application(JulyApplication) handles the request.
   The server can listen on other port, for example, you want a server that listens
   on port 5000, run `hello.py`::

    $ python hello.py --port=5000

   The default server is only accessible on your own computer, if you want to public
   it to users on your network, run `hello.py`::

    $ python hello.py --address=0.0.0.0

   Assumes that your IP Address is 192.168.0.10, your friends can get your message
   at `192.168.0.10:8000 <http://192.168.0.10:8000>`_ now.

2. URL Map provides a way the server response. Because there are many request,
   how could a server response the right data? URL Map solved this.
   You are browsing at the path /, the request sends a signal to the server
   that he is looking for page at path /. The server's application looks up its all
   handlers(URL Map), and finds the path / should be handled by ``HelloHandler``.

3. Handlers do the real work, they send the final results.


Create by Command-line
~~~~~~~~~~~~~~~~~~~~~~

The minimal project can be created by command::

    $ july startproject hello

It will create a folder called hello in the current directory, code in `hello/app.py`
is a little similar to this minimal application.


Debug Mode
-----------

Debug mode in tornado is very poor. But it will auto reload your application when code is
modified::

    application = JulyApplication(handlers=handlers, debug=True)


Rendering Template
-------------------

Writing HTML in python sucks, you cannot bear writting something like::

    class HomeHandler(JulyHandler):
        def get(self):
            self.write('<html>')
            self.write('<body>')
            ...
            self.write('</html>')

In this case, you need a template engine.

There are many template engines outside, like the famous Jinja, mako and etc. Feel free
to implement any of them to Tornado or July. But July use the tornado template engine,
because you can write python code in tornado template, you can do almost everything.

Access a template can be easy, folder structure::

    project/
        app.py
        templates/
            home.html

And in app.py::

    import os.path
    from july import JulyHandler, JulyApplication, run_server

    class HomeHandler(JulyHandler):
        def get(self, name):
            self.render('home.html', name=name)


    handlers = [
        ('/(.*)', HomeHandler),
    ]

    path = os.path.join(os.path.dirname(__file__), 'templates')
    application = JulyApplication(handlers=handlers, template_path=path)

    if __name__ == '__main__':
        run_server(application) 


And in home.html:

.. sourcecode:: html+jinja

    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Home</title>
    </head>
    <body>
        Hello {{ name }}
    </body>
    </html>


More on documentation at :ref:`template`.

Static Files
-------------

A web application always comes with static files, which means css and javascript. In
production, you can serve static files with nginx, but in development, you need an
easy solution::

    application = JulyApplication(handlers=handlers, static_path='path/to/static')

With ``july startproject``, you can get everything ready for your project.
A ``static`` folder is created under your project, and in app.py::

    settings = dict(
        static_path=os.path.join(ROOT, 'static'),
        static_url_prefix='/static/',
    )

    application = JulyApplication(handlers=handlers, **settings)


Now all your static files can be accessed at http://127.0.0.1:8000/static/

Static markup for your template::

    <link rel="stylesheet" href="{{ static_url('css/style.css') }}" />


Redirects and Errors
---------------------

::

    class TestHandler(JulyHandler):
        def get(self):
            self.redirect('/path/to/url')  #: redirect

            # errors
            # self.send_error(404)
            # self.send_error(403)


July App
----------

July App is a great way to organize your tornado project, it is much like blueprint in flask,
and a little similiar to Django App.

A glance at July App::

    app/
        __init__.py  <---- python package
        handlers.py  <---- name doesn't matter
        templates/   <---- name doesn't matter, maybe you don't need this


Simple example at `blog <https://github.com/lepture/july/tree/master/example/blog>`_ ,
the post folder is a July App::

    post_app = JulyApp('post', __name__, handlers=handlers, template_folder="templates")

You should always place your app and handlers at the very same file, the name doesn't matter,
you can name it anything you want.

Register the app to your project application::

    application.register_app(post_app, url_prefix='/post')


More documentation at :ref:`project-vs-app`
