import os.path
from tornado.web import Application, URLSpec
from july.util import get_root_path, import_object, ObjectDict


__all__ = ["JulyApp", "JulyApplication"]


class JulyApp(object):
    """July App

    July App is like BluePrint in Flask, it splits a tornado project into
    several apps.

    The basic usage, consider your app as::

        myapp/
            __init__.py
            handlers.py

    And in your ``myapp.handlers`` define::

        class MyHandler(RequestHandler):
            def get(self):
                self.write('hello july app')

        handlers = [
            ('/', MyHandler),
        ]

        app = JulyApp('a readable name', __name__, handlers=handlers)

        # you may also add a handler by ``app.add_handler``
        # app.add_handler(('/', MyHandler))

    .. admonition::

        You should always define an app in the same module level of your
        handlers. And it is suggested that you use ``__name__`` all the time.

    :param name: human readable name for the app

    :param template_folder:

        the folder name for templates in your app, for example, in your app::

            myapp/
                __init__.py
                handlers.py
                templates/

        so that template_folder is ``templates``. And you can define your app
        with app template supports::

            app = JulyApp('name', __name__, template_folder='templates')

    """
    _first_register = True

    def __init__(self, name, import_name, template_folder=None,
                 handlers=None, ui_modules=None, **settings):
        self.name = name
        self.import_name = import_name
        self.handlers = handlers
        self.ui_modules = ui_modules
        self.settings = settings
        self.root_path = get_root_path(self.import_name)

        if template_folder:
            self.template_path = os.path.join(self.root_path, template_folder)
        else:
            self.template_path = None

    def add_handler(self, handler):
        if self.handlers is None:
            self.handlers = [handler]
        else:
            self.handlers.append(handler)

    def register_filter(self, name, func):
        """Register filter function for template.

        .. admonition:: this filter can only be accessed in this app.
        """
        if '__july_filters__' not in self.settings:
            self.settings['__july_filters__'] = {}

        self.settings['__july_filters__'].update({name: func})

    def first_register(self):
        if not self._first_register:
            return False
        print('Register: %s' % self.name)
        self._first_register = False
        return True


class JulyApplication(object):
    """July Application

    This is a wrapper for ``tornado.web.Application``.
    You define a JulyApplication::

        application = JulyApplication()

    and when this application is called, it creates a tornado.web.Application,
    which means, JulyApplication()() equals to tornado.web.Application().

    so, you can do more with application before it is called.

    The most useful task for JulyApplication is registering a July App.
    Define you July App, and register it to your application::

        simple_app = JulyApp('name', __name__, handlers=handlers)
        application.register_app(simple_app)

    And start your application::

        application().listen(8888)
        ioloop.IOLoop.instance().start()
    """

    def __init__(self, handlers=None, default_host="", transforms=None,
                 wsgi=False, **settings):
        self.handlers = handlers
        self.default_host = default_host
        self.transforms = transforms
        self.wsgi = wsgi
        self.settings = settings

    def add_handler(self, handler):
        if not self.handlers:
            self.handlers = []

        self.handlers.append(handler)

    def add_ui_moudle(self, ui_module):
        if 'ui_modules' not in self.settings:
            self.settings['ui_modules'] = {}

        if ui_module:
            self.settings['ui_modules'].update(ui_module)

    def register_filter(self, name, func):
        """Register filter function for template::

            application = JulyApplication()
            application.register_filter('name', function)

        And it will be available in template::

            {{ name(var) }}

        The registered function can be accessed in all JulyHanlder
        subclass.
        """
        if '__july_filters__' not in self.settings:
            self.settings['__july_filters__'] = {}

        self.settings['__july_filters__'].update({name: func})

    def register_context(self, key, value):
        """Register global variables for template::

            application = JulyApplication()
            application.register_global('key', value)

        And it will be available in template::

            {{ g.key }}

        """
        if '__july_global__' not in self.settings:
            self.settings['__july_global__'] = ObjectDict()

        self.settings['__july_global__'][key] = value

    def register_app(self, app, url_prefix=''):
        if app.first_register():
            if '__july_apps__' not in self.settings:
                self.settings['__july_apps__'] = {}

            self.settings['__july_apps__'][app.import_name] = app
            self._register_app_handlers(app, url_prefix)
            self._register_app_ui_modules(app)

    def _register_app_handlers(self, app, url_prefix):
        if not app.handlers:
            return
        for spec in app.handlers:
            if isinstance(spec, tuple):
                assert len(spec) in (2, 3)
                pattern = spec[0]
                handler = spec[1]

                if isinstance(handler, str):
                    handler = import_object(handler)

                if len(spec) == 3:
                    kwargs = spec[2]
                else:
                    kwargs = {}

                pattern = '%s%s' % (url_prefix, pattern)
                spec = URLSpec(pattern, handler, kwargs)
            elif isinstance(spec, URLSpec):
                pattern = '%s%s' % (url_prefix, spec.regex.pattern)
                spec = URLSpec(pattern, spec.handler_class,
                               spec.kwargs, spec.name)

            self.add_handler(spec)

    def _register_app_ui_modules(self, app):
        self.add_ui_moudle(app.ui_modules)

    def __call__(self):
        app = Application(self.handlers, self.default_host, self.transforms,
                          self.wsgi, **self.settings)
        return app
