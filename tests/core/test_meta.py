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

from torneira import settings
from torneira.core import meta

class TimerProxyTestCase(unittest.TestCase):
            
    def test_timer_proxy_debug_true(self):
        
        settings.DEBUG = True

        fudge.clear_expectations()
        fudge.clear_calls()
        
        execute_fake = fudge.Fake(callable=True).with_args("shouldBeCursor", "shouldBeStatement", "shouldBeParameters", "shouldBeContext")        
        
        timerProxy = meta.TimerProxy()
        timerProxy.cursor_execute(execute_fake, "shouldBeCursor", "shouldBeStatement", "shouldBeParameters", "shouldBeContext", "shouldBeExecutemany")
        
        fudge.verify()

    @fudge.test
    def test_timer_proxy_debug_false(self):

        settings.DEBUG = False

        execute_fake = fudge.Fake(callable=True).with_args("shouldBeCursor", "shouldBeStatement", "shouldBeParameters", "shouldBeContext")        

        timerProxy = meta.TimerProxy()
        timerProxy.cursor_execute(execute_fake, "shouldBeCursor", "shouldBeStatement", "shouldBeParameters", "shouldBeContext", "shouldBeExecutemany")

class SessionTestCase(unittest.TestCase):
    @fudge.test
    def test_can_be_get_session(self):
        settings.DATABASE_ENGINE = "shouldBeDataBase"
        settings.DATABASE_POOL_SIZE = "shouldBePoolSize"
        
        FakeTimerProxy = fudge.Fake("TimerProxy").expects("__init__")
        timer_proxy_instance = FakeTimerProxy.returns_fake()

        create_engine_fake = fudge.Fake(callable=True).with_args("shouldBeDataBase", 
            pool_size="shouldBePoolSize", 
            pool_recycle=300, 
            proxy=timer_proxy_instance
        ).returns("shouldBeEngine")
        
        sessionmaker_fake = fudge.Fake(callable=True).with_args(autocommit=True, 
            autoflush=False, 
            expire_on_commit=False, 
            bind="shouldBeEngine"
        ).returns("shouldBeScopedSession")

        scoped_session_fake = fudge.Fake(callable=True).with_args("shouldBeScopedSession").returns("shouldBeSession")

        patches = [
            fudge.patch_object(meta, "TimerProxy", FakeTimerProxy),
            fudge.patch_object(meta, "create_engine", create_engine_fake),
            fudge.patch_object(meta, "sessionmaker", sessionmaker_fake),
            fudge.patch_object(meta, "scoped_session", scoped_session_fake)
        ]

        try:
            session = meta.TorneiraSession()
            self.assertEqual(session, "shouldBeSession")
        finally:
            
            for p in patches:
                p.restore()
