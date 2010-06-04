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
import cProfile as profile
from cStringIO import StringIO

import re, logging, sys

try:
    import settings
except ImportError, ie:
	logging.warn("Not found settings file, using settings default!")
	import settings_default as settings
	
COOKIE_SECRET = "29NbhyfgaA092ZkjMbNvCx06789jdA8iIlLqz7d1D9c8"

class TorneiraServer(Daemon):
    
    def __init__(self, pidfile, port, project_root, media_dir):
        self.port = port
        self.project_root = project_root
        self.media_dir = media_dir
        
        return Daemon.__init__(self, pidfile)

    def run(self):
    
        application = Application([
            (r"/media/(.*)", StaticFileHandler, {"path": self.media_dir}),
            (r"/.*", TorneiraHandler)
        ], cookie_secret=COOKIE_SECRET)
        
        http_server = HTTPServer(application)
        http_server.listen(self.port)
        
        logging.info("Torneira Server START! listening port %s " % self.port)
        
        IOLoop.instance().start()
        
class TorneiraHandler(RequestHandler):

    def process_request(self, *args, **kargs):
        mapper = TorneiraDispacther().getMapper()
        
        # remove get args
        uri = re.sub("\?.*", "", self.request.uri)

        match = mapper.match(uri)
        if match:
            try:
                controller = TorneiraDispatcher().getController(match['controller'])
                controller.handler = self

                response = getattr(controller, match['action'])(**self.prepared_arguments(match))
                
                if not response: return
                self.write(response)
            
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
            self.process_request(*args, **kw)
    
    def post(self, *args, **kw):
        logging.debug("POST %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request(*args, **kw)

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

