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

from torneira.settings import settings
from torneira.core import dispatcher

urls = [("url_name", "url_route", "controller", "action")]

class DispatcherTestCase(unittest.TestCase):

    def setUp(self):
        settings.ROOT_URLS = "unit.core.test_dispatcher"
    
    def tearDown(self):
        settings.ROOT_URLS = ""
    
    def test_can_be_get_urls(self):
        dp = dispatcher.TorneiraDispatcher()
        self.assertEqual(dp.getUrls(), urls)
    
    def test_can_be_get_mapper(self):

        fudge.clear_expectations()
        FakeMapper = fudge.Fake("Mapper").expects("__init__")
        fake_instance = FakeMapper.returns_fake().expects('connect').with_args("url_name", "url_route", controller="controller", action="action")
        
        with fudge.patched_context(dispatcher, "Mapper", FakeMapper):

            dp = dispatcher.TorneiraDispatcher()
            mapper = dp.getMapper()
        
        self.assertEqual(fake_instance, mapper)
        fudge.clear_calls()
    
    def test_can_be_get_controller(self):

        fudge.clear_expectations()
        controller = fudge.Fake().provides("__init__").has_attr(__name__="shouldBeName")
        controller_intance = controller.returns_fake()

        dp = dispatcher.TorneiraDispatcher()
        ctrl = dp.getController(controller)

        self.assertEqual(controller_intance, ctrl)
        self.assertEqual(dp.__controllers__, {"shouldBeName":ctrl})
        fudge.clear_calls()
        
    def test_can_be_create_url(self):
        
        url = dispatcher.url(route="shouldBeRoute", controller="shouldBeController", action="shouldBeAction", name="shouldBeName")
        self.assertEqual(url, ['shouldBeName', 'shouldBeRoute', 'shouldBeController', 'shouldBeAction'])
        