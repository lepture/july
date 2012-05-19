#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging
import smtplib
from email.MIMEText import MIMEText
from email.utils import formatdate, parseaddr
from tornado.escape import utf8

from tornado.options import options

#: define these options yourself
SMTP_USER = options.smtp_user
SMTP_PASSWORD = options.smtp_password
SMTP_HOST = options.smtp_host
SMTP_DURATION = int(options.smtp_duration)

_session = None


__all__ = ['send_mail', 'Message']


def send_mail(user, subject, body, **kwargs):
    """send mail

    If you want to send html email, set subtype to html::

        send_mail(user, subject, body, subtype='html')
    """
    message = Message(user, subject, body, **kwargs)
    msg = message.as_msg()
    msg['From'] = SMTP_USER

    SMTP_FROM = parseaddr(SMTP_USER)[1]

    global _session
    if _session is None:
        _session = _SMTPSession(
            SMTP_HOST, SMTP_FROM, SMTP_PASSWORD, SMTP_DURATION
        )

    _session.send_mail(SMTP_FROM, message.email, msg.as_string())


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
    def __init__(self, host, user='', password='', duration=30, ssl=True):
        self.host = host
        self.user = user
        self.password = password
        self.duration = duration
        self.ssl = ssl

        self.renew()

    def send_mail(self, fr, to, message):
        if self.timeout:
            self.renew()

        try:
            self.session.sendmail(fr, to, message)
        except Exception, e:
            err = "Send email from %s to %s failed!\n Exception: %s!" \
                % (fr, to, e)
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
