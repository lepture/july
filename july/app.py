import os.path
from tornado.web import Application, URLSpec
from july.util import get_root_path, import_object


__all__ = ["JulyApp", "JulyApplication"]


class JulyApp(object):
    _first_register = True

    def __init__(self, name, import_name, template_folder=None,
                 handlers=[], ui_modules={}):
        self.name = name
        self.import_name = import_name
        self.handlers = handlers
        self.ui_modules = ui_modules
        self.root_path = get_root_path(self.import_name)

        if template_folder:
            self.template_path = os.path.join(self.root_path, template_folder)
        else:
            self.template_path = None

    def first_register(self):
        if not self._first_register:
            return False
        print('Register: %s' % self.name)
        self._first_register = False
        return True


class JulyApplication(object):
    """July Application
    """

    def __init__(self, handlers=None, default_host="", transforms=None,
                 wsgi=False, **settings):
        self.handlers = handlers
        self.default_host = default_host
        self.transforms = transforms
        self.wsgi = wsgi
        self.settings = settings

    def register_app(self, app, url_prefix=''):
        if app.first_register():
            if 'app_list' not in self.settings:
                self.settings['app_list'] = {}

            self.settings['app_list'][app.import_name] = app
            self.register_app_handlers(app, url_prefix)
            self.register_app_ui_modules(app)

    def register_app_handlers(self, app, url_prefix):
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

                pattern = '/%s%s' % (url_prefix, pattern)
                spec = URLSpec(pattern, handler, kwargs)
            elif isinstance(spec, URLSpec):
                pattern = '/%s%s' % (url_prefix, spec.regex.pattern)
                spec = URLSpec(pattern, spec.handler_class,
                               spec.kwargs, spec.name)

            self.register_handler(spec)

    def register_app_ui_modules(self, app):
        self.register_ui_moudle(app.ui_modules)

    def register_handler(self, handler):
        if not self.handlers:
            self.handlers = []

        self.handlers.append(handler)

    def register_ui_moudle(self, ui_module):
        if 'ui_modules' not in self.settings:
            self.settings['ui_modules'] = {}

        self.settings['ui_modules'].update(ui_module)

    def __call__(self):
        app = Application(self.handlers, self.default_host, self.transforms,
                          self.wsgi, **self.settings)
        return app
