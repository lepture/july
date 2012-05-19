# -*- coding: utf-8 -*-

import logging
from tornado.web import URLSpec as url
from july.web import JulyHandler
from july.app import JulyApp
from lib import send_mail


class MailHandler(JulyHandler):
    def check_xsrf_cookie(self):
        #: disable xsrf cookie check
        return

    def post(self):
        #: provide as a service
        #: only the server has access to this service
        if self.request.remote_ip != '127.0.0.1':
            self.send_error(403)
            return
        user = self.get_argument('user', None)
        subject = self.get_argument('subject', None)
        body = self.get_argument('body', '')
        subtype = self.get_argument('subtype', 'plain')
        if not (user and subject):
            self.send_error(403)
            logging.warn('Send mail without user or subject')
            return
        try:
            send_mail(user, subject, body, subtype=subtype)
        except Exception as e:
            logging.error(e)

        self.write('')


mail_app = JulyApp(
    'mail', __name__,
    handlers=[url('/outbox', MailHandler, name='mail-outbox')]
)
