from july.app import JulyApp, JulyApplication
from nose.tools import raises


class TestJulyApp(object):
    def setUp(self):
        self.app = JulyApp('test', __name__)

    def test_first_register(self):
        assert self.app.first_register() == True
        assert self.app.first_register() == False

    def test_add_handler(self):
        self.app.add_handler(('/', 'TestJulyApp'))
        assert self.app.handlers == [('/', 'TestJulyApp')]

    def test_register_filter(self):
        assert '__july_filters__' not in self.app.settings
        self.app.register_filter('min', min)
        assert '__july_filters__' in self.app.settings


class TestJulyApplication(object):
    def setUp(self):
        self.application = JulyApplication()

    def test_register_context(self):
        self.application.register_context('key', 'value')
        assert self.application.settings['__july_global__']['key'] == 'value'

    def test_register_filter(self):
        self.application.register_filter('min', min)

    @raises(ImportError)
    def test_register_app1(self):
        app = JulyApp('app1', __name__)
        app.add_handler(('', 'joking'))
        self.application.register_app(app, '/app')

    def test_register_app2(self):
        #: app without handlers
        app = JulyApp('app2', 'app2')
        assert '__july_apps__' not in self.application.settings
        self.application.register_app(app, '/app')
