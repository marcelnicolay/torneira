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

from mox import Mox
from torneira.core import dispatcher

urls = [("url_name", "url_route", "controller", "action", "module")]

def test_can_be_load_dispatcher():
	mox = Mox()

	mox.ReplayAll()
	try:
		_dispatcher = dispatcher.TorneiraDispatcher()
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_be_get_urls():
	mox = Mox()

	mox.StubOutWithMock(dispatcher, "settings", use_mock_anything=True)
	dispatcher.settings.ROOT_URLS = 'unit.core.test_dispatcher'

	_dispatcher = dispatcher.TorneiraDispatcher()

	mox.ReplayAll()
	try:
		assert urls == _dispatcher.getUrls()
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_be_get_mapper():
	mox = Mox()

	mox.StubOutWithMock(dispatcher, "settings", use_mock_anything=True)
	mox.StubOutWithMock(dispatcher, "Mapper", use_mock_anything=True)

	dispatcher.settings.ROOT_URLS = 'unit.core.test_dispatcher'

	mapper_mock = mox.CreateMockAnything()
	mapper_mock.connect('url_name', 'url_route', action='action', controller='module.controller')

	dispatcher.Mapper().AndReturn(mapper_mock)

	_dispatcher = dispatcher.TorneiraDispatcher()

	mox.ReplayAll()
	try:
		assert mapper_mock == _dispatcher.getMapper()
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()
