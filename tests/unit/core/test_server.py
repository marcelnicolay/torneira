from mox import Mox
from torneira.core import server

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
