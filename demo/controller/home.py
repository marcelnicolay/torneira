# coding: utf-8
from torneira import __version__
from torneira.controller import BaseController


class HomeController(BaseController):
    _teste = None

    def initialize(self, *args, **kwargs):
        super(HomeController, self).initialize(*args, **kwargs)
        self._teste = 'WORKS! ;)'

    def index(self):
        #return "Torneira v%s" % __version__
        return self.render_to_template("home.html", version=__version__)

    def custom(self):
        return "%s - Torneira v%s" % (self._teste, __version__)
