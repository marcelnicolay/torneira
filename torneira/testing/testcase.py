# coding: utf-8
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from torneira import settings


class TestCase(AsyncHTTPTestCase):
    def get_app(self):
        _imported = __import__(settings.ROOT_URLS, globals(), locals(), ['urls'], -1)
        return Application(_imported.urls, cookie_secret='123456')
