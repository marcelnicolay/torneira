# coding: utf-8
from torneira import __version__
from torneira.controller import BaseController


class HomeController(BaseController):
    _teste = None

    def initialize(self, *args, **kwargs):
        super(HomeController, self).initialize(*args, **kwargs)
        self._teste = 'WORKS! ;)'

    def index(self, request_handler):
        return self.render_to_template("home.html", version=__version__)

    def json_service(self, request_handler):
        return {'torneira': {'version': __version__}}

    def custom(self, request_handler):
        return "%s - Torneira v%s" % (self._teste, __version__)
