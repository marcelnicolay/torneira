# coding: utf-8
from tornado.web import url

from more_complex_app.handlers import MainHandler


urls = (
    url(r'/', MainHandler, {'action': 'index'}),
    url(r'/simple', MainHandler, {'action': 'simple'}),
    url(r'/json', MainHandler, {'action': 'as_json'}),
    url(r'/async', MainHandler, {'action': 'async'}),
)
