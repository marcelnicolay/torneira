# coding: utf-8
from tornado.web import url

from simple_app.handlers import MainHandler


urls = (
    url(r'/', MainHandler, {'action': 'index'}),
)
