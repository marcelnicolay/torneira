# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import with_statement
import urllib

import fudge
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, url

from torneira.controller import BaseController, render_to_extension
from tests.util import unittest

try:
    # Python >= 2.6
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

# simplexml module is optional
try:
    import simplexml
except ImportError:
    simplexml = None

try:
    import json
except ImportError:
    import simplejson as json


class SimpleController(BaseController):
    def index(self, *args, **kwargs):
        if 'request_handler' in kwargs:
            response = 'request_handler received'
        else:
            response = 'request_handler not received'
        return response

    def post_data(self, request_handler, *args, **kwargs):
        response = []
        for key, value in kwargs.iteritems():
            if type(value) == list:
                for v in value:
                    response.append((key, v))
            else:
                response.append((key, value))
        return urllib.urlencode(response)

    def render_json(self, request_handler, *args, **kwargs):
        response = [
            {'a': 1},
            {'b': 2},
        ]
        return self.render_to_json(response, request_handler)

    def render_xml(self, request_handler, *args, **kwargs):
        response = {
            'root': {
                'a': 1,
                'b': 2,
            }
        }
        return self.render_to_xml(response, request_handler)

    def render_response_error(self, request_handler, *args, **kwargs):
        message = 'error!'
        return self.render_error(message)

    def render_response_success(self, request_handler, *args, **kwargs):
        message = 'success!'
        return self.render_success(message)

    @render_to_extension
    def render_to_extension_with_decorator(self, request_handler, *args, **kwargs):
        return {'root': {'key': 'value'}}


urls = (
    url(r'/controller/simple/', SimpleController, {'action': 'index'}),
    url(r'/controller/post-data/', SimpleController, {'action': 'post_data'}),
    url(r'/controller/render-json/', SimpleController, {'action': 'render_json'}),
    url(r'/controller/render-xml/', SimpleController, {'action': 'render_xml'}),
    url(r'/controller/render-error/', SimpleController, {'action': 'render_response_error'}),
    url(r'/controller/render-success/', SimpleController, {'action': 'render_response_success'}),
    url(r'/controller/render-to-extension\.(?P<extension>[a-z]*)', SimpleController, {'action': 'render_to_extension_with_decorator'}),
)
app = Application(urls, cookie_secret='secret')


class BaseControllerTestCase(AsyncHTTPTestCase, unittest.TestCase):
    def get_app(self):
        return app

    def test_controller_method_must_receive_request_handler_as_kwarg(self):
        response = self.fetch('/controller/simple/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'request_handler received')

    def test_post_data_should_be_received_in_kwargs(self):
        post_data = (
            ('a_list', 1),
            ('a_list', 2),
            ('a_list', 3),
            ('single_value', 'value'),
            ('another_single_value', 'value 2'),
        )
        post_body = urllib.urlencode(post_data)
        response = self.fetch('/controller/post-data/', method='POST', body=post_body)
        self.assertEqual(response.code, 200)
        self.assertEqual(parse_qs(response.body), parse_qs(post_body))

    def test_render_to_json_should_return_json_response(self):
        response = self.fetch('/controller/render-json/')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
        self.assertEqual(response.code, 200)

        expected = [
            {'a': 1},
            {'b': 2},
        ]
        parsed_response = json.loads(response.body)
        self.assertEqual(parsed_response, expected)

    @unittest.skipUnless(simplexml, "simplexml module not installed")
    def test_render_to_xml_should_return_xml_response(self):
        response = self.fetch('/controller/render-xml/')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'text/xml; charset=UTF-8')
        self.assertEqual(response.code, 200)

        expected = {
            'root': {
                'a': '1',
                'b': '2',
            }
        }
        parsed_response = simplexml.loads(response.body)
        self.assertEqual(parsed_response, expected)

    def test_render_response_error_should_return_preformatted_json(self):
        response = self.fetch('/controller/render-error/')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
        self.assertEqual(response.code, 200)

        expected = {
            'errors': {
                'error': {
                    'message': 'error!'
                }
            }
        }
        parsed_response = json.loads(response.body)
        self.assertEqual(parsed_response, expected)

    def test_render_response_success_should_return_preformatted_json(self):
        response = self.fetch('/controller/render-success/')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
        self.assertEqual(response.code, 200)

        expected = {
            'errors': '',
            'message': 'success!'
        }
        parsed_response = json.loads(response.body)
        self.assertEqual(parsed_response, expected)

    @fudge.patch('torneira.controller.base.locale',
                 'torneira.controller.base.settings')
    def test_if_can_setup_tornado_locale_module(self, locale, settings):
        LOCALE = {
            'code': 'pt_BR',
            'path': 'locales/',
            'domain': 'appname',
        }
        settings.has_attr(LOCALE=LOCALE)

        (locale
            .is_a_stub()
            .expects('set_default_locale')
            .with_args('pt_BR')
            .expects('load_gettext_translations')
            .with_args('locales/', 'appname'))

        response = self.fetch('/controller/simple/')
        self.assertEqual(response.code, 200)

    @fudge.patch('torneira.controller.base.settings')
    def test_raise_assertexception_if_settings_locale_was_not_configured(self, settings):
        settings.has_attr(LOCALE={})

        with self.assertRaises(AssertionError):
            response = self.fetch('/controller/simple/')
            self.assertEqual(response.code, 200)


class RenderToExtensionDecoratorTestCase(AsyncHTTPTestCase):
    EXPECTED_RESPONSE = {'root': {'key': 'value'}}

    def get_app(self):
        return app

    def test_render_response_without_specifying_extension_should_return_json(self):
        response = self.fetch('/controller/render-to-extension.')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
        self.assertEqual(response.code, 200)
        parsed_response = json.loads(response.body)
        self.assertEqual(parsed_response, self.EXPECTED_RESPONSE)

    def test_render_response_as_json(self):
        response = self.fetch('/controller/render-to-extension.json')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
        self.assertEqual(response.code, 200)
        parsed_response = json.loads(response.body)
        self.assertEqual(parsed_response, self.EXPECTED_RESPONSE)

    def test_render_response_as_jsonp(self):
        response = self.fetch('/controller/render-to-extension.jsonp?callback=cb')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/javascript; charset=UTF-8')
        self.assertEqual(response.code, 200)
        expected_response = "cb(%s);" % json.dumps(self.EXPECTED_RESPONSE)
        self.assertEqual(response.body, expected_response)

    @unittest.skipUnless(simplexml, "simplexml module not installed")
    def test_render_response_as_xml(self):
        response = self.fetch('/controller/render-to-extension.xml')
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'text/xml; charset=UTF-8')
        self.assertEqual(response.code, 200)
        parsed_response = simplexml.loads(response.body)
        self.assertEqual(parsed_response, self.EXPECTED_RESPONSE)
