#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate, parseaddr
from tornado.escape import utf8
from tornado.options import options

from july.util import set_default_option
set_default_option('smtp_user', 'root@localhost')
set_default_option('smtp_password', '')
set_default_option('smtp_host', 'localhost')
set_default_option('smtp_ssl', False)


_session = None


__all__ = ['send_mail', 'Message']


def send_mail(user, subject, body, **kwargs):
    """send mail

    If you want to send html email, set subtype to html::

        send_mail(user, subject, body, subtype='html')
    """
    message = Message(user, subject, body, **kwargs)
    msg = message.as_msg()
    msg['From'] = options.smtp_user

    global _session
    if _session is None:
        _session = _SMTPSession()

    _session.send_mail(message.email, msg.as_string())


class Message(object):
    def __init__(self, user, subject, body, **kwargs):
        self.user = user  # lepture <lepture@me.com>
        self.name, self.email = parseaddr(user)
        self.subject = subject
        self.body = body
        self.subtype = kwargs.pop('subtype', 'plain')
        self.date = kwargs.pop('date', None)

    def as_msg(self):
        msg = MIMEText(utf8(self.body), self.subtype)
        msg.set_charset('utf-8')
        msg['To'] = utf8(self.email)
        msg['Subject'] = utf8(self.subject)
        if self.date:
            msg['Date'] = self.date
        else:
            msg['Date'] = formatdate()
        return msg


class _SMTPSession(object):
    def __init__(self, duration=30):
        self.host = options.smtp_host
        self.user = parseaddr(options.smtp_user)[1]
        self.password = options.smtp_password
        self.duration = duration
        self.ssl = options.smtp_ssl

        self.renew()

    def send_mail(self, to, message):
        if self.timeout:
            self.renew()

        try:
            self.session.sendmail(self.user, to, message)
        except Exception as e:
            err = "Send email from %s to %s failed!\n Exception: %s!" \
                % (self.user, to, e)
            logging.error(err)

    @property
    def timeout(self):
        if datetime.utcnow() < self.deadline:
            return False
        else:
            return True

    def renew(self):
        try:
            self.session.quit()
        except Exception:
            pass

        if self.ssl:
            self.session = smtplib.SMTP_SSL(self.host)
        else:
            self.session = smtplib.SMTP(self.host)
        if self.user and self.password:
            self.session.login(self.user, self.password)

        self.deadline = datetime.utcnow() + \
                timedelta(seconds=self.duration * 60)
