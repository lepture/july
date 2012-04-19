from tornado import web, escape
from july.template import JulyTemplateLoader

__all__ = ["JulyHandler", "ApiHandler", "UIModule", "run_server"]


class JulyHandler(web.RequestHandler):
    """July Handler

    Subclass JulyHandler to make an app, it provides a way to organize a July
    App, and will support more features in the future.
    """
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
        settings = self.settings
        if '__july_apps__' in settings and self.app_template:
            app = settings['__july_apps__'].get(self.__module__, None)
            if app:
                kwargs = {}
                if 'autoescape' in settings:
                    kwargs['autoescape'] = settings['autoescape']

                return JulyTemplateLoader(template_path, app, **kwargs)
        return super(JulyHandler, self).create_template_loader(template_path)


class ApiHandler(web.RequestHandler):
    xsrf_protect = False

    def check_xsrf_cookie(self):
        if not self.xsrf_protect:
            return
        return super(ApiHandler, self).check_xsrf_cookie()

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
        super(ApiHandler, self).write(chunk)


class UIModule(web.UIModule):
    @property
    def db(self):
        return self.handler.db

    @property
    def cache(self):
        return self.handler.cache


def run_server(app):
    import logging
    import tornado.locale
    from tornado import httpserver, ioloop
    from tornado.options import options, parse_command_line
    from july.util import parse_config_file

    parse_command_line()
    if options.settings:
        parse_config_file(options.settings)

    server = httpserver.HTTPServer(app(), xheaders=True)
    server.listen(int(options.port), options.address)

    if options.locale_path:
        tornado.locale.load_translations(options.locale_path)
        tornado.locale.set_default_locale(options.default_locale)

    logging.info('Start server at %s:%s' % (options.address, options.port))
    ioloop.IOLoop.instance().start()
