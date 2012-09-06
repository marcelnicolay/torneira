# coding: utf-8
import os

import fudge
from tornado.web import Application, url
from tornado.testing import AsyncHTTPTestCase

from torneira.handler import TorneiraHandler
from torneira.template.mako_engine import MakoMixin


class SimpleHandler(TorneiraHandler):
    def index(self):
        self.write("output from simple handler")

    def another_action(self):
        self.write("output from another action")

    def action_returns_something(self):
        return 'returned output'

    def put(self):
        self.write("output from put method")


class MakoTemplateHandler(TorneiraHandler, MakoMixin):
    def index(self):
        context = {
            'variable_name': 'variable value',
        }
        return self.render_to_template('template.html', **context)

    def unknown_template(self):
        self.render_to_template('unknown-template.html')


urls = (
    url(r'/simple/', SimpleHandler, {'action': 'index'}),
    url(r'/without-action/', SimpleHandler),
    url(r'/another-action/', SimpleHandler, {'action': 'another_action'}),
    url(r'/should-return-something/', SimpleHandler, {'action': 'action_returns_something'}),
    url(r'/mako-mixin/', MakoTemplateHandler, {'action': 'index'}),
    url(r'/mako-mixin/unknown-template/', MakoTemplateHandler, {'action': 'unknown_template'}),
)
app = Application(urls, cookie_secret='secret')
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')


class TorneiraHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app

    def test_make_get_request_should_call_correct_action(self):
        response = self.fetch('/simple/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'output from simple handler')

    def test_make_get_request_without_action_and_custom_get_should_return_500(self):
        response = self.fetch('/without-action/')
        self.assertEqual(response.code, 500)

    def test_make_get_request_to_another_url_should_call_correct_action(self):
        response = self.fetch('/another-action/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'output from another action')

    def test_make_request_to_action_should_write_returned_content_to_server_output(self):
        response = self.fetch('/should-return-something/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'returned output')

    def test_make_post_request_should_call_correct_action(self):
        response = self.fetch('/simple/', method='POST', body='key=value')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'output from simple handler')

    def test_make_put_request_should_call_default_put_method_from_tornado(self):
        response = self.fetch('/without-action/', method='PUT', body='key=value')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'output from put method')


class MakoTemplateHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app

    def test_make_request_without_template_dirs_settings_should_return_500(self):
        response = self.fetch('/mako-mixin/')
        self.assertEqual(response.code, 500)

    @fudge.patch('torneira.template.mako_engine.settings')
    def test_make_request_for_unknown_template_should_return_500(self, settings):
        settings.has_attr(TEMPLATE_DIRS=(ASSETS_DIR,))
        response = self.fetch('/mako-mixin/unknown-template/')
        self.assertEqual(response.code, 500)

    @fudge.patch('torneira.template.mako_engine.settings')
    def test_make_request_should_render_template_with_params(self, settings):
        settings.has_attr(TEMPLATE_DIRS=(ASSETS_DIR,))
        response = self.fetch('/mako-mixin/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, u'template text em português (variable value)\n'.encode('utf-8'))


class ProfilerHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app

    @fudge.patch('torneira.handler.settings',
                 'torneira.handler.Profile')
    def test_enable_profile_request_should_call_profile_class(self, settings, Profile):
        settings.has_attr(PROFILING=True, PROFILE_FILE='profile_filename.out')

        (Profile
            .is_callable()
            .returns_fake()
            .expects('runcall')
            .calls(lambda method, *a, **kw: method(*a, **kw))
            .expects('dump_stats')
            .with_args('profile_filename.out'))

        response = self.fetch('/simple/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'output from simple handler')
