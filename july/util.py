from __future__ import with_statement
import os
import sys
import pkgutil
from tornado.options import define, options


def set_default_option(name, default=None, **kwargs):
    if name in options:
        return
    define(name, default, **kwargs)


def parse_config_file(path):
    config = {}
    exec(compile(open(path).read(), path, 'exec'), config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])


class ObjectDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


def import_object(name, arg=None):
    """tornado.util.import_object replacement for july project

    .. attention:: you should not use this function
    """

    if '.' not in name:
        return __import__(name)
    parts = name.split('.')
    try:
        obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    except ImportError:
        obj = None
    return getattr(obj, parts[-1], arg)


def get_root_path(import_name):
    """Returns the path to a package or cwd if that cannot be found.  This
    returns the path of a package or the folder that contains a module.

    Not to be confused with the package path returned by :func:`find_package`.
    """
    loader = pkgutil.get_loader(import_name)
    if loader is None or import_name == '__main__':
        # import name is not found, or interactive/main module
        return os.getcwd()
    # For .egg, zipimporter does not have get_filename until Python 2.7.
    if hasattr(loader, 'get_filename'):
        filepath = loader.get_filename(import_name)
    else:
        # Fall back to imports.
        __import__(import_name)
        filepath = sys.modules[import_name].__file__
    # filepath is import_name.py for a module, or __init__.py for a package.
    return os.path.dirname(os.path.abspath(filepath))
