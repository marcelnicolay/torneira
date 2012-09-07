# coding: utf-8
from torneira import __version__
from torneira.handler import TorneiraHandler
from torneira.template import MakoMixin


class HomeHandler(TorneiraHandler, MakoMixin):
    _teste = None

    def initialize(self, *args, **kwargs):
        super(HomeHandler, self).initialize(*args, **kwargs)
        self._teste = 'WORKS! ;)'

    def index(self):
        return self.render_to_template("home.html", version=__version__)

    def json_service(self):
        return {'torneira': {'version': __version__}}

    def custom(self):
        return "%s - Torneira v%s" % (self._teste, __version__)
