import sae
from tornado.options import options
from sqlalchemy.pool import NullPool
options.sqlalchemy_master = 'mysql://%s:%s@%s:%s/%s?charset=utf8' %\
        (sae.const.MYSQL_USER, sae.const.MYSQL_PASS, sae.const.MYSQL_HOST,
         sae.const.MYSQL_PORT, sae.const.MYSQL_DB)

options.sqlalchemy_kwargs = {
    'poolclass': NullPool,
}

from july import JulyHandler, JulyApplication
from july.database import db


class HomeHandler(JulyHandler):
    def get(self):
        db._ping_db()
        self.write('hello world')


handlers = [
    ('/', HomeHandler),
]

app = JulyApplication(handlers, wsgi=True, debug=True)
