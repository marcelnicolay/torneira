# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler, RequestHandler, HTTPError
from tornado.ioloop import IOLoop
from torneira.controller import BaseController
from torneira.core.daemon import Daemon
from torneira.core.dispatcher import TorneiraDispatcher
from torneira import settings

import cProfile as profile
from cStringIO import StringIO

import re, logging, sys, functools

class TorneiraServer(Daemon):

    def __init__(self, pidfile, port, media_dir, xheaders=False):
        self.port = port
        self.media_dir = media_dir
        self.xheaders = xheaders

        return Daemon.__init__(self, pidfile)

    def run(self):

        cookie_secret = settings.COOKIE_SECRET if hasattr(settings, 'COOKIE_SECRET') else None
        application = Application([
            (r"/media/(.*)", StaticFileHandler, {"path": self.media_dir}),
            (r"/.*", TorneiraHandler)
        ], cookie_secret=cookie_secret, debug=settings.DEBUG)

        http_server = HTTPServer(application, xheaders=self.xheaders)
        http_server.listen(self.port)

        logging.info("Torneira Server START! listening port %s " % self.port)

        IOLoop.instance().start()

class TorneiraHandler(RequestHandler):

    def process_request(self, method='GET', *args, **kargs):
        mapper = TorneiraDispatcher().getMapper()

        # remove get args
        uri = re.sub("\?.*", "", self.request.uri)

        match = mapper.match(uri)
        if match:
            try:
                controller = TorneiraDispatcher().getController(match['controller'])

                action = match['action']

                if not action:
                    action = {'GET':'index','POST':'create','PUT':'update','DELETE':'delete'}.get(method, 'index')
                    
                karguments = self.prepared_arguments(match)
                karguments['request_handler'] = self
                
                response = getattr(controller, action)(**karguments)

                if not response: return
                self.write(response)

            except HTTPError, he:
                logging.exception("Erro lancado")
                raise he
            except Exception, e:
                logging.exception("500 - Erro ao processar a requisicao %s" % e)
                if settings.DEBUG:
                    raise HTTPError(500)
                else:
                    self.write(BaseController().render_to_template("/500.html"))
        else:
            logging.exception("404 - Pagina nao encontrada %s" % self.request.uri)
            if settings.DEBUG:
                raise HTTPError(404)
            else:
                self.write(BaseController().render_to_template("/404.html"))

    def get(self, *args, **kw):
        logging.debug("GET %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request('GET',*args, **kw)

    def post(self, *args, **kw):
        logging.debug("POST %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request('POST', *args, **kw)

    def put(self, *args, **kw):
        logging.debug("PUT %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request('PUT', *args, **kw)

    def delete(self, *args, **kw):
        logging.debug("DELETE %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request('DELETE', *args, **kw)

    def options(self, *args, **kw):
        logging.debug("OPTIONS %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request('OPTIONS', *args, **kw)

    def prepared_arguments(self, match):
        arguments = {}
        for arg,value in self.request.arguments.iteritems():
            arguments[arg] = value[0]

        for key,value in match.iteritems():
            if key not in ('controller','action'):
                arguments[key] = value

        return arguments

    def profiling(self, *args, **kw):
        self.profiler = profile.Profile()

        self.profiler.runcall(self.process_request, *args, **kw)

        self.profiler.dump_stats(settings.PROFILE_FILE)

def asynchronous(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        request_handler = kwargs.get('request_handler')
        if not request_handler:
            raise Exception("@asynchronous require request_handler parameter")

        request_handler._auto_finish = False
        return method(self, *args, **kwargs)
    return wrapper