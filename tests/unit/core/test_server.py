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
from torneira.core import server
import tornado.web

class ServerTestCase(unittest.TestCase):
    
    def test_can_be_run(self):
        
        fudge.clear_expectations()
        fudge.clear_calls()
        
        FakeApplication = fudge.Fake("Application").expects("__init__").with_args([
            (r"/media/(.*)", tornado.web.StaticFileHandler, {"path": "shouldBeMediaDir"}),
            (r"/.*", server.TorneiraHandler)
        ], cookie_secret=settings.COOKIE_SECRET)
        
        application_instance = FakeApplication.returns_fake()
        
        FakeServer = fudge.Fake("HTTPServer").expects("__init__").with_args(application_instance)
        server_instance = FakeServer.returns_fake().expects("listen").with_args("shouldBePort")
        
        FakeIOLoop = fudge.Fake("IOLoop").expects("instance")
        FakeIOLoop.returns_fake().expects("start")
        
        patches = [
            fudge.patch_object(server, "Application", FakeApplication),
            fudge.patch_object(server, "HTTPServer", FakeServer),
            fudge.patch_object(server, "IOLoop", FakeIOLoop)
        ]
        
        try:
            torneira_server = server.TorneiraServer("shouldBePidfile", "shouldBePort", "shouldBeRoot", "shouldBeMediaDir")
            
            self.assertEqual(torneira_server.pidfile, "shouldBePidfile")
            self.assertEqual(torneira_server.project_root, "shouldBeRoot")
            self.assertEqual(torneira_server.media_dir, "shouldBeMediaDir")
            
            torneira_server.run()
            
        finally:
            fudge.verify()
            
            for p in patches:
                p.restore()
        
class RequestHandlerTestCase(unittest.TestCase):
    
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()
        
        self.application_fake = fudge.Fake().has_attr(ui_methods={}, ui_modules={})
        self.request_fake = fudge.Fake().has_attr(uri="shouldBeUri").provides("supports_http_1_1").returns(True)
        
    def tearDown(self):
        fudge.verify()
        
    def test_can_be_handler_get(self):
                
        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        process_request_fake = fudge.Fake(callable=True).with_args('GET', "shouldBeArgs", shouldBeNamedParam="value")
        
        with fudge.patched_context(handler, "process_request", process_request_fake):
        
            handler.get("shouldBeArgs", shouldBeNamedParam="value")
            
    def test_can_be_handler_post(self):

        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        process_request_fake = fudge.Fake(callable=True).with_args('POST', "shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "process_request", process_request_fake):
            handler.post("shouldBeArgs", shouldBeNamedParam="value")       
            
    def test_can_be_handler_put(self):

        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        process_request_fake = fudge.Fake(callable=True).with_args('PUT', "shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "process_request", process_request_fake):
            handler.put("shouldBeArgs", shouldBeNamedParam="value")
            
    def test_can_be_handler_delete(self):
        
        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        process_request_fake = fudge.Fake(callable=True).with_args('DELETE', "shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "process_request", process_request_fake):
            handler.delete("shouldBeArgs", shouldBeNamedParam="value")

    def test_can_be_handler_profiling_get(self):

        settings.PROFILING = True
        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        profiling_fake = fudge.Fake(callable=True).with_args("shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "profiling", profiling_fake):

            handler.get("shouldBeArgs", shouldBeNamedParam="value")

        settings.PROFILING = False

    def test_can_be_handler_profiling_post(self):

        settings.PROFILING = True
        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        profiling_fake = fudge.Fake(callable=True).with_args("shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "profiling", profiling_fake):

            handler.post("shouldBeArgs", shouldBeNamedParam="value")

        settings.PROFILING = False

    def test_can_be_handler_profiling_put(self):

        settings.PROFILING = True
        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        profiling_fake = fudge.Fake(callable=True).with_args("shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "profiling", profiling_fake):

            handler.put("shouldBeArgs", shouldBeNamedParam="value")

        settings.PROFILING = False

    def test_can_be_handler_profiling_delete(self):

        settings.PROFILING = True
        handler = server.TorneiraHandler(self.application_fake, self.request_fake)
        profiling_fake = fudge.Fake(callable=True).with_args("shouldBeArgs", shouldBeNamedParam="value")

        with fudge.patched_context(handler, "profiling", profiling_fake):

            handler.delete("shouldBeArgs", shouldBeNamedParam="value")

        settings.PROFILING = False
