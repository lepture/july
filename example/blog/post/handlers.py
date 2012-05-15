# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from tornado.options import options
    options.sqlalchemy_master = 'sqlite:////tmp/demo.sqlite'

from july import JulyHandler, JulyApp
from july.database import db
from tornado.web import URLSpec as url
from models import Post


class CreateHandler(JulyHandler):
    def get(self):
        self.render('inner/create.html')

    def post(self):
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        post = Post(title=title, content=content)

        db.master.add(post)
        db.master.commit()
        self.redirect(self.reverse_url('post', post.id))


class PostHandler(JulyHandler):
    def get(self, id):
        post = Post.query.filter_by(id=id).first()
        if not post:
            self.send_error(404)
            return
        self.render('post.html', post=post)


handlers = [
    ('/create', CreateHandler),
    url('/(\d+)', PostHandler, name='post'),
]

post_app = JulyApp('post', __name__, handlers=handlers,
                   template_folder="templates")


if __name__ == '__main__':
    from july import run_server, JulyApplication
    run_server(JulyApplication(handlers=handlers, debug=True,
                               template_path="templates"))
