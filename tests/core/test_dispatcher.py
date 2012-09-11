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
from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase
from torneira.controller import BaseController
from torneira.core.dispatcher import url


class SimpleController(BaseController):
    def index(self, *args, **kwargs):
        return 'index ok'

    def with_parameter(self, param, request_handler):
        return "action_with_parameter " + param

    def preserve_url_name(self, request_handler):
        return request_handler.reverse_url('name-of-url')


urls = (
    url('/controller/simple/', SimpleController, action='index', name='index'),
    url('/controller/parameter/{param}', SimpleController, action='with_parameter', name='with_parameter'),
    url('/controller/preserve-name/', SimpleController, action='preserve_url_name', name='name-of-url'),
)
app = Application(urls, cookie_secret='secret')


class DispatcherTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app

    def test_use_routes_for_map_a_simple_url(self):
        response = self.fetch('/controller/simple/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'index ok')

    def test_use_routes_for_map_a_url_with_parameter(self):
        response = self.fetch('/controller/parameter/shouldBeParam')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'action_with_parameter shouldBeParam')

    def test_use_routes_for_mapping_urls_should_preserve_the_name_of_url(self):
        response = self.fetch('/controller/preserve-name/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, r'/controller/preserve-name/')
