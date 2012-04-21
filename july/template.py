import os.path
from tornado.template import Loader, Template


class JulyTemplateLoader(Loader):
    """July Template Loader
    """

    def __init__(self, root_directory, app, **kwargs):
        super(JulyTemplateLoader, self).__init__(root_directory, **kwargs)
        self.app = app

    def _create_template(self, name):
        path = self._detect_template_path(name)
        if not path:
            raise IOError("Can't find file: %s" % name)
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
        path = os.path.join(self.root, name)
        if os.path.exists(path):
            return path

        if self.app.template_path:
            path = os.path.join(self.app.template_path, name)
            if os.path.exists(path):
                return path

        return None
