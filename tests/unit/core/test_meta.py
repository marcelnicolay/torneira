from mox import Mox
from torneira.core import server

def test_can_be_load_server():
	_server = server.TorneiraServer("pidfile", 8080, "project_root", "media_dir")
	assert _server.pidfile == "pidfile"
	assert _server.port == 8080
	assert _server.project_root == "project_root"
	assert _server.media_dir == "media_dir"
