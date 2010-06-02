from mox import Mox
from torneira.core import dispatcher

def test_can_be_load_dsipatcher():
	mox = Mox()

	mox.ReplayAll()
	try:
		_dispatcher = dispatcher.TorneiraDispatcher()
		mox.VerifyAll()
	finally:
		mox.UnsetStubs()
