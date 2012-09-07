# coding: utf-8
from torneira import __version__
from torneira.handler import TorneiraHandler


class MainHandler(TorneiraHandler):
    def index(self):
        return "You are running Torneira v%s" % __version__
