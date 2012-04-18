from july import JulyHandler, JulyApp


class HomeHandler(JulyHandler):
    def get(self):
        self.render('myapp/home.html')


handlers = [
    ('/', HomeHandler),
]

myapp = JulyApp('myapp', __name__, handlers=handlers,
                template_folder="templates")
