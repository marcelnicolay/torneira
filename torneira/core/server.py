# -*- coding: utf-8 -*-
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import cProfile as profile

from tornado.web import Application, HTTPError, StaticFileHandler, RequestHandler, URLSpec
from tornado.ioloop import IOLoop

from torneira.core.daemon import Daemon
from torneira import settings


class TorneiraServer(Daemon):

    def __init__(self, pidfile, port, media_dir, xheaders=False):
        self.port = port
        self.media_dir = media_dir
        self.xheaders = xheaders
        self.urls = self._get_urls()

        return Daemon.__init__(self, pidfile)

    def _get_urls(self):
        _imported = __import__(settings.ROOT_URLS, globals(), locals(), ['urls'], -1)
        return _imported.urls

    def run(self):

        cookie_secret = settings.COOKIE_SECRET if hasattr(settings, 'COOKIE_SECRET') else None
        static_url = URLSpec(r"/media/(.*)", StaticFileHandler, {"path": self.media_dir}),
        urls = static_url + self.urls
        application = Application(urls, cookie_secret=cookie_secret,
                debug=settings.DEBUG, xheaders=self.xheaders)

        application.listen(self.port)

        logging.info("Torneira Server START! listening port %s " % self.port)

        IOLoop.instance().start()


class TorneiraHandler(RequestHandler):
    _action = None

    def initialize(self, action=None):
        self._action = action

    def process_request(self, method='GET', *args, **kwargs):
        if not self._action:
            raise HTTPError(500, 'Misconfigured server: action not informed')

        method_callable = getattr(self, self._action)
        return method_callable(*args, **kwargs)

    def get(self, *args, **kw):
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            response = self.process_request('GET', *args, **kw)
            if response:
                self.write(response)

    def post(self, *args, **kw):
        logging.debug("POST %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            response = self.process_request('POST', *args, **kw)
            if response:
                self.write(response)

    def put(self, *args, **kw):
        logging.debug("PUT %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            response = self.process_request('PUT', *args, **kw)
            if response:
                self.write(response)

    def delete(self, *args, **kw):
        logging.debug("DELETE %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            response = self.process_request('DELETE', *args, **kw)
            if response:
                self.write(response)

    def prepared_arguments(self, match):
        arguments = {}
        for arg, value in self.request.arguments.iteritems():
            arguments[arg] = value[0]

        for key, value in match.iteritems():
            if key not in ('controller', 'action'):
                arguments[key] = value

        return arguments

    def profiling(self, *args, **kw):
        self.profiler = profile.Profile()

        self.profiler.runcall(self.process_request, *args, **kw)

        self.profiler.dump_stats(settings.PROFILE_FILE)
