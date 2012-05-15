import os.path
from tornado.template import BaseLoader, Template


class JulyLoader(BaseLoader):
    """July Template Loader
    """

    def __init__(self, roots, **kwargs):
        super(JulyLoader, self).__init__(**kwargs)
        if isinstance(roots, basestring):
            self.roots = [roots]
        else:
            assert isinstance(roots, (list, tuple)), "roots should be lists"
            self.roots = roots

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        path = self._detect_template_path(name)
        f = open(path, 'r')
        template = Template(f.read(), name=name, loader=self)
        f.close()
        return template

    def _detect_template_path(self, name):
        """
        First load template from project templates directory.

        If template not in project templates directory, load from app templates
        directories.

        Directory example of an app::

            app/
                templates/
                    appname/   <---- better with an appname
                        layout.html
                        screen.html

        """
        for root in self.roots:
            path = os.path.join(root, name)
            if os.path.exists(path):
                return path

        return name
