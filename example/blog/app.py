#!/usr/bin/env python
# -*- coding: utf-8 -*-

from july import JulyHandler, JulyApplication, run_server

from tornado.options import options
options.sqlalchemy_master = 'sqlite:////tmp/demo.sqlite'

import os.path
ROOT = os.path.abspath(os.path.dirname(__file__))
from post.models import Post
from post.handlers import post_app


class HomeHandler(JulyHandler):
    def get(self):
        posts = Post.query.all()
        self.render('home.html', posts=posts)


handlers = [
    ('/', HomeHandler),
]


settings = dict(
    template_path=os.path.join(ROOT, 'templates'),
    static_path=os.path.join(ROOT, 'static'),
    static_url_prefix='/static/',
)

application = JulyApplication(handlers=handlers, debug=True, **settings)

application.register_app(post_app, url_prefix='/post')

if __name__ == '__main__':
    run_server(application)
