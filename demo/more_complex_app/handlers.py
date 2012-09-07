# coding: utf-8
from tornado.web import asynchronous
from torneira import __version__
from torneira.handler import TorneiraHandler
from torneira.template import MakoMixin


class MainHandler(TorneiraHandler, MakoMixin):
    def index(self):
        return self.render_to_template('index.html')

    def simple(self):
        return "You can use self.write or just returns the contents"

    def as_json(self):
        return {'json_response': [1, 2, 3]}

    @asynchronous
    def async(self):
        context = {'version': __version__}
        content = self.render_to_template('async.html', **context)
        self.write(content)
        self.finish()
