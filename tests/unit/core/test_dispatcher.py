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
