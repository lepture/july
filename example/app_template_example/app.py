from july import JulyApplication, run_server
from myapp.handlers import myapp

from tornado.web import RequestHandler


class HomeHandler(RequestHandler):
    def get(self):
        self.write('hello')


handlers = [
    ('/', HomeHandler),
]

application = JulyApplication(handlers=handlers, debug=True)
application.register_app(myapp, url_prefix='/app')

run_server(application)
