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

import unittest, fudge

from torneira.controller import base

class BaseControllerTestCase(unittest.TestCase):
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()

    def tearDown(self):
        fudge.verify()

    def test_if_can_setup_tornado_locale_module(self):
        """Tests if the torneira is setting up tornado.locale correctly"""

        class settings_mock:
            LOCALE = {
                'code': 'pt_BR',
                'path': 'locales/',
                'domain': 'appname',
            }

        locale_mock = fudge.Fake().is_a_stub() \
            .expects('set_default_locale') \
            .with_args('pt_BR') \
            .expects('load_gettext_translations') \
            .with_args('locales/', 'appname')

        base_controller = base.BaseController()
        with fudge.patched_context(base, "settings", settings_mock):
            with fudge.patched_context(base, 'locale', locale_mock):
                base_controller.setup_locale()

    def test_raise_assertexception_if_settings_locale_was_not_configured(self):
        class settings_mock:
            LOCALE = {}

        base_controller = base.BaseController()
        with fudge.patched_context(base, "settings", settings_mock):
            with self.assertRaises(AssertionError):
                base_controller.setup_locale()
