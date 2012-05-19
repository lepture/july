import urllib
from tornado import escape
from tornado import httpclient
from tornado.options import options


__all__ = ['post']


def post(path, args, callback=None):
    url = 'http://127.0.0.1:%s/%s' % (options.port, path)
    http = httpclient.AsyncHTTPClient()
    post_args = {}
    for key in args:
        #: ensure encodings
        post_args[key] = escape.utf8(args[key])

    http.fetch(url, method="POST", body=urllib.urlencode(post_args),
               callback=callback)
