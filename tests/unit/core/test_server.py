from mox import Mox
from torneira.core import server
from tornado.web import HTTPError
from nose.tools import assert_equals, assert_raises

def test_can_be_load_server():
	_server = server.TorneiraServer("pidfile", 8080, "project_root", "media_dir")
	assert _server.pidfile == "pidfile"
	assert _server.port == 8080
	assert _server.project_root == "project_root"
	assert _server.media_dir == "media_dir"
	
def test_can_be_run():
	mox = Mox()
	
	mox.StubOutWithMock(server, "Application", use_mock_anything=True)
	mox.StubOutWithMock(server, "StaticFileHandler", use_mock_anything=True)
	mox.StubOutWithMock(server, "TorneiraHandler", use_mock_anything=True)
	mox.StubOutWithMock(server, "HTTPServer", use_mock_anything=True)
	mox.StubOutWithMock(server, "IOLoop", use_mock_anything=True)
	
	_server = server.TorneiraServer("pidfile", 8080, "should-be-project-root", "should-be-media-dir")
	
	application_mock = mox.CreateMockAnything()
	http_server_mock = mox.CreateMockAnything()
	
	server.TorneiraHandler = "should-be-torneirahandler"
	server.StaticFileHandler = "should-be-filehandler"
	server.Application([
			(r"/media/(.*)", "should-be-filehandler", {"path": "should-be-media-dir"}),
            (r"/.*", "should-be-torneirahandler")
    ], cookie_secret=server.COOKIE_SECRET).AndReturn(application_mock)

	server.HTTPServer(application_mock).AndReturn(http_server_mock)
	
	http_server_mock.listen(8080)
	
	ioloop_mock = mox.CreateMockAnything()
	ioloop_mock.start()
	
	server.IOLoop.instance().AndReturn(ioloop_mock)
	
	mox.ReplayAll()
	try:
		
		_server.run()
		
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_handler_get():
	mox = Mox()

	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.supports_http_1_1().AndReturn(True)
	
	process_request_mock = mox.CreateMockAnything()
	process_request_mock(**{'arg':'should-be-args'})
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.process_request = process_request_mock				

		handler.get(arg='should-be-args')
		
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()
	
def test_can_handler_post():
	mox = Mox()

	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.supports_http_1_1().AndReturn(True)
	
	process_request_mock = mox.CreateMockAnything()
	process_request_mock(**{'arg':'should-be-args'})
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.process_request = process_request_mock				

		handler.post(arg='should-be-args')
		
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_handler_profiling_get():
	mox = Mox()

	mox.StubOutWithMock(server, "settings", use_mock_anything=True)
	server.settings.PROFILING = True
	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.supports_http_1_1().AndReturn(True)
	
	profiling_mock = mox.CreateMockAnything()
	profiling_mock(**{'arg':'should-be-args'})
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.profiling = profiling_mock				

		handler.get(arg='should-be-args')
		
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()
	
def test_can_handler_profiling_post():
	mox = Mox()

	mox.StubOutWithMock(server, "settings", use_mock_anything=True)
	server.settings.PROFILING = True
	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.supports_http_1_1().AndReturn(True)
	
	profiling_mock = mox.CreateMockAnything()
	profiling_mock(**{'arg':'should-be-args'})
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.profiling = profiling_mock

		handler.post(arg='should-be-args')
		
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_handler_process_request_match():
	mox = Mox()
	
	mox = Mox()

	mox.StubOutWithMock(server, "TorneiraDispatcher", use_mock_anything=True)

	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.uri = "/should-be-uri.html"
	request_mock.supports_http_1_1().AndReturn(True)
	
	match_value = {'controller':'should-be-controller','action':'shouldBeAction'}
	
	prepared_arguments_mock = mox.CreateMockAnything()
	prepared_arguments_mock(match_value).AndReturn({'arg':'value'})
	
	mapper_mock = mox.CreateMockAnything()
	mapper_mock.match("/should-be-uri.html").AndReturn(match_value)
	
	controller_mock = mox.CreateMockAnything()
	controller_mock.shouldBeAction(arg='value').AndReturn("shoul-be-response")
	
	dispatcher_mock = mox.CreateMockAnything()
	dispatcher_mock.getMapper().AndReturn(mapper_mock)
	dispatcher_mock.getController('should-be-controller').AndReturn(controller_mock)
	
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	
	write_mock = mox.CreateMockAnything()
	write_mock("shoul-be-response")
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.prepared_arguments = prepared_arguments_mock
		handler.write = write_mock
		handler.process_request()
			
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()
	
def test_can_handler_process_request_raise500():
	mox = Mox()
	
	mox = Mox()

	mox.StubOutWithMock(server, "TorneiraDispatcher", use_mock_anything=True)

	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.uri = "/should-be-uri.html"
	request_mock.supports_http_1_1().AndReturn(True)
	
	match_value = {'controller':'should-be-controller','action':'shouldBeAction'}
	
	prepared_arguments_mock = mox.CreateMockAnything()
	prepared_arguments_mock(match_value).AndReturn({'arg':'value'})
	
	mapper_mock = mox.CreateMockAnything()
	mapper_mock.match("/should-be-uri.html").AndReturn(match_value)
	
	controller_mock = mox.CreateMockAnything()
	controller_mock.shouldBeAction(arg='value').AndRaise(Exception)
	
	dispatcher_mock = mox.CreateMockAnything()
	dispatcher_mock.getMapper().AndReturn(mapper_mock)
	dispatcher_mock.getController('should-be-controller').AndReturn(controller_mock)
	
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.prepared_arguments = prepared_arguments_mock
		assert_raises(HTTPError, handler.process_request)
			
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_handler_process_request_render_500_template():
	mox = Mox()

	mox.StubOutWithMock(server, "TorneiraDispatcher", use_mock_anything=True)
	mox.StubOutWithMock(server, "BaseController", use_mock_anything=True)
	mox.StubOutWithMock(server, "settings", use_mock_anything=True)
	
	server.settings.DEBUG = False

	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.uri = "/should-be-uri.html"
	request_mock.supports_http_1_1().AndReturn(True)
	
	match_value = {'controller':'should-be-controller','action':'shouldBeAction'}
	
	prepared_arguments_mock = mox.CreateMockAnything()
	prepared_arguments_mock(match_value).AndReturn({'arg':'value'})
	
	mapper_mock = mox.CreateMockAnything()
	mapper_mock.match("/should-be-uri.html").AndReturn(match_value)
	
	controller_mock = mox.CreateMockAnything()
	controller_mock.shouldBeAction(arg='value').AndRaise(Exception)
	
	dispatcher_mock = mox.CreateMockAnything()
	dispatcher_mock.getMapper().AndReturn(mapper_mock)
	dispatcher_mock.getController('should-be-controller').AndReturn(controller_mock)
	
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	
	base_controller_mock = mox.CreateMockAnything()
	base_controller_mock.render_to_template("/500.html").AndReturn("should-be-500-response")
	server.BaseController().AndReturn(base_controller_mock)
	write_mock = mox.CreateMockAnything()
	write_mock("should-be-500-response")


	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.prepared_arguments = prepared_arguments_mock
		handler.write = write_mock
		handler.process_request()
			
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_handler_process_request_raise404():
	mox = Mox()

	mox.StubOutWithMock(server, "TorneiraDispatcher", use_mock_anything=True)

	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.uri = "/should-be-uri.html"
	request_mock.supports_http_1_1().AndReturn(True)
	
	mapper_mock = mox.CreateMockAnything()
	mapper_mock.match("/should-be-uri.html").AndReturn(False)
	
	dispatcher_mock = mox.CreateMockAnything()
	dispatcher_mock.getMapper().AndReturn(mapper_mock)
	
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	
	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		assert_raises(HTTPError, handler.process_request)
			
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()

def test_can_handler_process_request_render_404_template():
	mox = Mox()

	mox.StubOutWithMock(server, "TorneiraDispatcher", use_mock_anything=True)
	mox.StubOutWithMock(server, "BaseController", use_mock_anything=True)
	mox.StubOutWithMock(server, "settings", use_mock_anything=True)
	
	server.settings.DEBUG = False
	
	application_mock = mox.CreateMockAnything()
	application_mock.ui_methods = {}
	application_mock.ui_modules = {}	
	
	request_mock = mox.CreateMockAnything()
	request_mock.uri = "/should-be-uri.html"
	request_mock.supports_http_1_1().AndReturn(True)
	
	mapper_mock = mox.CreateMockAnything()
	mapper_mock.match("/should-be-uri.html").AndReturn(False)
	
	dispatcher_mock = mox.CreateMockAnything()
	dispatcher_mock.getMapper().AndReturn(mapper_mock)
	
	server.TorneiraDispatcher().AndReturn(dispatcher_mock)
	
	base_controller_mock = mox.CreateMockAnything()
	base_controller_mock.render_to_template("/404.html").AndReturn("should-be-404-response")
	server.BaseController().AndReturn(base_controller_mock)
	write_mock = mox.CreateMockAnything()
	write_mock("should-be-404-response")

	mox.ReplayAll()

	try:
		handler = server.TorneiraHandler(application_mock, request_mock)
		handler.write = write_mock
		handler.process_request()
			
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()
