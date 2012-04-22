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
    app = JulyApplication(handlers=handlers)

    if __name__ == '__main__':
        from july import run_server
        run_server(app)

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

The minimal project can be created by comman::

    $ july startproject hello

It will create a folder called hello in the current directory, code in `hello/app.py`
is a little similar to this minimal application.


Template
----------

Static
--------
