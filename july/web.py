#!/usr/bin/python
"""July Application Wrapper

July Application Wrapper provides a good way to organize your tornado app
like blueprints or Django.

:copyright: (c) 2012 by lepture
:license: BSD
"""

import os

#: always use utc time
os.environ['TZ'] = 'UTC'

#: always place python3 egg cache in /tmp
os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"

from tornado.options import define, options

_first_run = True
if _first_run:
    #: server configuration
    define('debug', default=True, type=bool, help='show debug information')
    define('port', default=5000, type=int, help='run server on this port')
    define('settings', default='', type=str, help='setting file path')

    #: application configuration
    define('template_path', type=str,
           help='absolute path of template directory')
    define('static_path', type=str, help='absolute path of static directory')
    define('static_url_prefix', default='/static/', type=str)
    define('enable_app_static', default=True, type=bool)
    define('xsrf_cookies', default=False, type=bool)
    define('cookie_secret', type=str)

    define('locale_path', type=str, help='absolute path of locale directory')
    define('default_locale', default='en_US', type=str)

    define('login_url', default='/account/login', type=str,
           help='when use is not authenticated, redirect to login_url')

    define('api_prefix', default='/api/', type=str)

    _first_run = False


import logging
from tornado import web, escape
from tornado.util import import_object
from tornado.template import Loader, Template
from july.util import parse_config_file


def register_app(app_list):
    """Detect if an app is available"""
    for app in app_list:
        name = app[0]
        app = app[1]
        if '.' in app:
            module = import_object(app)
        else:
            module = __import__(app)

        if hasattr(module, '__appname__'):
            name = module.__appname__
        if hasattr(module, '__version__'):
            version = module.__version__
        else:
            version = '1.0'

        logging.info("Loading: %s (%s)", name, version)
        if hasattr(module, 'requirements'):
            requires = ', '.join(module.requirements)
            logging.info("%s requires: %s", name, requires)


def register_app_handlers(handlers, app_list):
    """Register the app to handlers from app_list.

    Define your app_list at your project config.py file::

        app_list = [
            ('appname', 'yourproject.yourapp'),
            (...),
        ]

    And in yourproject/yourapp/handlers.py, define urls as usual. This
    function will create the new pattern of urls for you. An example::

        #: `~yourproject.yourapp.handlers.urls`
        urls = [
            ('/create', CreateHandler),  # a tuple
            url('/delete', DeleteHandler, name='delete'),  # URLSpec
            (...),
        ]

    Tuple and URLSpec are accepted like default tornado does. And the
    final urls will be something like::

        /appname/create
        /appname/delete
        /appname/...
    """
    if not app_list:
        return
    for app in app_list:
        try:
            app_handlers = import_object('%s.handlers.urls' % app[1])
        except AttributeError:
            app_handlers = []
        except ImportError:
            app_handlers = []
        for spec in app_handlers:
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

                pattern = '/%s/%s' % (app[0], pattern.lstrip('/'))
                spec = web.URLSpec(pattern, handler, kwargs)
            elif isinstance(spec, web.URLSpec):
                pattern = '/%s/%s' % (app[0], spec.regex.pattern.lstrip('/'))
                spec = web.URLSpec(pattern, app[1], spec.kwargs, spec.name)

            handlers.append(spec)


def register_app_ui_modules(ui_modules, app_list):
    """Register the app to ui_modules from app_list.

    Define your app_list at your project config.py file::

        app_list = [
            ('appname', 'yourproject.yourapp'),
            (...),
        ]

    And in yourproject/yourapp/handlers.py, define ui_modules as usual::

        #: `~yourproject.yourapp.handlers.ui_modules`
        ui_modules = {
            'MyModule': MyUIModule,
            ...
        }

    """
    if not app_list:
        return
    for app in app_list:
        try:
            app_modules = import_object('%s.handlers.ui_modules' % app[1])
        except AttributeError:
            app_modules = {}
        except ImportError:
            app_modules = {}
        ui_modules.update(app_modules)


def register_app_api(handlers, app_list):
    """Register the app's api to handlers from app_list.

    Define your app_list at your project config.py file::

        app_list = [
            ('appname', 'yourproject.yourapp'),
            (...),
        ]

    And in yourproject/yourapp/api.py, define urls as usual. This
    function will create the new pattern of urls for you. An example::

        #: `~yourproject.yourapp.api.urls`
        urls = [
            ('/create', CreateHandler),  # a tuple
        ]

    Tuple and URLSpec are accepted like default tornado does. And the
    final urls will be something like::

        /api/appname/create
    """
    if not app_list:
        return
    api_prefix = options.api_prefix.rstrip('/')
    for app in app_list:
        try:
            app_handlers = import_object('%s.api.urls' % app[1])
        except AttributeError:
            app_handlers = []
        except ImportError:
            app_handlers = []
        for spec in app_handlers:
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

                pattern = '%s/%s/%s' % \
                        (api_prefix, app[0], pattern.lstrip('/'))
                spec = web.URLSpec(pattern, handler, kwargs)
            elif isinstance(spec, web.URLSpec):
                pattern = '%s/%s/%s' % \
                        (api_prefix, app[0], spec.regex.pattern.lstrip('/'))
                spec = web.URLSpec(pattern, app[1], spec.kwargs, spec.name)

            handlers.append(spec)


class JulyTemplateLoader(Loader):
    def __init__(self, root_directory, app_list, **kwargs):
        super(JulyTemplateLoader, self).__init__(root_directory, **kwargs)
        self.app_list = app_list

    def _create_template(self, name):
        path = self._detect_template_path(name)
        if not path:
            raise OSError("Can't find file: %s" % name)
        f = open(path, 'r')
        template = Template(f.read(), name=name, loader=self)
        f.close()
        return template

    def _detect_template_path(self, name):
        """
        First load template from project templates directory.

        If template not in project templates directory, load from app templates
        directories.

        Directory example of an app::

            app/
                templates/
                    appname/   <---- better with an appname
                        layout.html
                        screen.html

        """
        path = os.path.join(self.root, name)
        if os.path.exists(path):
            return path
        for app in self.app_list:
            app = app[1]
            if '.' in app:
                app_path = import_object(app).__path__[0]
            else:
                app_path = __import__(app).__path__[0]
            path = os.path.join(app_path, 'templates', name)
            if os.path.exists(path):
                return path

        return None


class JulyApplication(web.Application):
    """July Application
    """
    def __init__(self, handlers=[], default_host="", transforms=None,
                 wsgi=False, **settings):
        try:
            import config
        except ImportError:
            config = None
        db = getattr(config, 'db', None)
        cache = getattr(config, 'cache', None)
        app_list = getattr(config, 'app_list', [])

        try:
            import urls
        except ImportError:
            urls = None

        try:
            handlers.extend(urls.handlers)
        except AttributeError:
            pass
        register_app_handlers(handlers, app_list)
        register_app_api(handlers, app_list)

        try:
            ui_modules = urls.ui_modules
        except AttributeError:
            ui_modules = {}
        register_app_ui_modules(ui_modules, app_list)

        settings.update(dict(
            debug=options.debug,
            login_url=options.login_url,

            cookie_secret=options.cookie_secret,
            xsrf_cookies=options.xsrf_cookies,

            template_path=options.template_path,
            static_path=options.static_path,
            static_url_prefix=options.static_url_prefix,

            ui_modules=ui_modules,
            app_list=app_list,
        ))

        if hasattr(options, 'autoescape'):
            settings['autoescape'] = options.autoescape

        super(JulyApplication, self).__init__(handlers, default_host,
                                              transforms, wsgi, **settings)

        if db:
            JulyApplication.db = db.session
        else:
            JulyApplication.db = None
        JulyApplication.cache = cache

    def load_app_static(self, handlers, app_list):
        #TODO
        pass


class JulyHandler(web.RequestHandler):
    app_template = True

    @property
    def db(self):
        if hasattr(self.application, 'db'):
            return self.application.db
        return None

    @property
    def cache(self):
        if hasattr(self.application, 'cache'):
            return self.application.cache
        return None

    def create_template_loader(self, template_path):
        settings = self.application.settings
        if 'app_list' not in settings or not self.app_template:
            return super(JulyHandler,
                         self).create_template_loader(template_path)
        kwargs = {}
        if 'autoescape' in settings:
            kwargs['autoescape'] = settings['autoescape']
        return JulyTemplateLoader(template_path, settings['app_list'],
                                  **kwargs)


class JsonHandler(web.RequestHandler):
    xsrf_protect = False

    def check_xsrf_cookie(self):
        if not self.xsrf_protect:
            return
        return super(JsonHandler, self).check_xsrf_cookie()

    def is_ajax(self):
        return "XMLHttpRequest" == self.request.headers.get("X-Requested-With")

    def write(self, chunk):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        if isinstance(chunk, (dict, list)):
            chunk = escape.json_encode(chunk)
            callback = self.get_argument('callback', None)
            if callback:
                chunk = "%s(%s)" % (callback, escape.to_unicode(chunk))
                self.set_header("Content-Type",
                                "application/javascript; charset=UTF-8")
        super(JsonHandler, self).write(chunk)


class UIModule(web.UIModule):
    @property
    def db(self):
        return self.handler.db

    @property
    def cache(self):
        return self.handler.cache


def run_server(app_func):
    import tornado.options
    import tornado.locale
    from tornado import httpserver, ioloop

    tornado.options.parse_command_line()
    if options.settings:
        parse_config_file(options.settings)

    server = httpserver.HTTPServer(app_func(), xheaders=True)
    server.listen(int(options.port))

    if options.locale_path:
        tornado.locale.load_translations(options.locale_path)
        tornado.locale.set_default_locale(options.default_locale)

    try:
        import config
    except ImportError:
        config = None
    app_list = getattr(config, 'app_list', [])
    register_app(app_list)
    logging.info('Start server at 0.0.0.0:%s' % options.port)
    ioloop.IOLoop.instance().start()
