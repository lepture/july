
from junetornado.web import JuneHandler


class HomeHandler(JuneHandler):
    def get(self):
        self.render('myapp/home.html')


urls = [
    ('/', HomeHandler),
]
