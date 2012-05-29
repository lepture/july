#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.options import define
define('smtp_user', 'root@gmail.com')
define('smtp_password', 'password')
define('smtp_host', 'smtp.gmail.com')
define('smtp_ssl', True)

from july.web import JulyHandler, run_server
from july.app import JulyApplication
from july.ext import webservice

import os.path
ROOT = os.path.abspath(os.path.dirname(__file__))


class HomeHandler(JulyHandler):
    def get(self):
        self.render('home.html')

    def post(self):
        user = self.get_argument('user')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        dct = dict(user=user, subject=subject, body=body, subtype='html')
        self.redirect('/')
        webservice.post('mail/outbox', dct)


handlers = [
    ('/', HomeHandler),
]


settings = dict(
    template_path=os.path.join(ROOT, 'templates'),
)

application = JulyApplication(handlers=handlers, debug=True, **settings)

application.register_app('july.ext.mail.handlers.app', url_prefix='/mail')

if __name__ == '__main__':
    run_server(application)
