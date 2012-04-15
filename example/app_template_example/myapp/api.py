from july import JulyHandler


class HomeHandler(JulyHandler):
    def get(self):
        self.render('myapp/home.html')


urls = [
    ('', HomeHandler),
]
