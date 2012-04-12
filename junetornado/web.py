#!/usr/bin/python
"""June Application Wrapper

June Application Wrapper provides a good way to organize your tornado app
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

#: server configuration
define('debug', default=True, type=bool, help='show debug information')
define('port', default=5000, type=int, help='run server on this port')

#: application configuration
define('template_path', type=str, help='absolute path of template directory')
define('static_path', type=str, help='absolute path of static directory')
define('static_url_prefix', default='/static/', type=str)
define('enable_app_static', default=True, type=bool)
define('xsrf_cookies', default=False, type=bool)
define('cookie_secret', type=str)

define('locale_path', type=str, help='absolute path of locale directory')

define('login_url', default='/account/login', type=str,
       help='when use is not authenticated, redirect to login_url')


from tornado import web, escape
from tornado.util import import_object
from tornado.template import Loader, Template


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
    for app in app_list:
        try:
            app_handlers = import_object('%s.handlers.urls' % app[1])
        except AttributeError:
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

                pattern = '/%s%s' % (app[0], pattern)
                spec = web.URLSpec(pattern, handler, kwargs)
            elif isinstance(spec, web.URLSpec):
                pattern = '/%s%s' % (app[0], spec.regex.pattern)
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
    for app in app_list:
        try:
            app_modules = import_object('%s.handlers.ui_modules' % app[1])
        except AttributeError:
            app_modules = {}
        ui_modules.update(app_modules)


class JuneTemplateLoader(Loader):
    def __init__(self, root_directory, app_list, **kwargs):
        super(JuneTemplateLoader, self).__init__(root_directory, **kwargs)
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


class JuneApplication(web.Application):
    """June Application
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

        handlers.extend(getattr(urls, 'handlers', []))
        register_app_handlers(handlers, app_list)

        ui_modules = getattr(urls, 'ui_modules', {})
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

        super(JuneApplication, self).__init__(handlers, default_host,
                                              transforms, wsgi, **settings)

        if db:
            JuneApplication.db = db.session
        else:
            JuneApplication.db = None
        JuneApplication.cache = cache

        if options.locale_path:
            #TODO: load app locale
            self.load_locale()

    def load_locale(self):
        import tornado.locale
        tornado.locale.load_translations(options.locale_path)
        tornado.locale.set_default_locale(options.default_locale)

    def load_app_static(self, handlers, app_list):
        #TODO
        pass


class JuneHandler(web.RequestHandler):
    app_template = False

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
        if 'app_list' not in settings:
            return super(JuneHandler,
                         self).create_template_loader(template_path)
        kwargs = {}
        if 'autoescape' in settings:
            kwargs['autoescape'] = settings['autoescape']
        return JuneTemplateLoader(template_path, settings['app_list'],
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


def run_server(app):
    import tornado.options
    from tornado import httpserver, ioloop
    define('settings', '')
    tornado.options.parse_command_line()
    server = httpserver.HTTPServer(app, xheaders=True)
    server.listen(int(options.port))
    print('Start server at 0.0.0.0:%s' % options.port)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    class HomeHandler(JuneHandler):
        def get(self):
            self.write('hello world')

    handlers = [('/', HomeHandler)]
    app = JuneApplication(handlers)
    run_server(app)
