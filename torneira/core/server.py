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
        self.setup_locale()

    def define_current_locale(self, locale_code):
        self._current_locale = locale.get(locale_code)

    def setup_locale(self):        
        if not hasattr(settings, 'LOCALE'):
            return
            
        assert settings.LOCALE.has_key('code')
        assert settings.LOCALE.has_key('path')
        assert settings.LOCALE.has_key('domain')

        locale_code = settings.LOCALE['code']
        locale.set_default_locale(locale_code)
        locale.load_gettext_translations(settings.LOCALE['path'],
                                         settings.LOCALE['domain'])
        self.define_current_locale(locale_code)

    def get_translate(self):
        if not self._current_locale:
            return lambda s: s
        else:
            return self._current_locale.translate

    def process_request(self, method='GET', *args, **kwargs):
        if not self._action:
            raise HTTPError(500, 'Misconfigured server: action not informed')

        method_callable = getattr(self, self._action)
        if settings.PROFILING:
            return self.profiling(method_callable, *args, **kwargs)
        else:
            return method_callable(*args, **kwargs)

    def get(self, *args, **kw):
        response = self.process_request('GET', *args, **kw)
        if response:
            self.write(response)

    def post(self, *args, **kw):
        logging.debug("POST %s processing..." % self.request.uri)
        response = self.process_request('POST', *args, **kw)
        if response:
            self.write(response)

    def put(self, *args, **kw):
        logging.debug("PUT %s processing..." % self.request.uri)
        response = self.process_request('PUT', *args, **kw)
        if response:
            self.write(response)

    def delete(self, *args, **kw):
        logging.debug("DELETE %s processing..." % self.request.uri)
        response = self.process_request('DELETE', *args, **kw)
        if response:
            self.write(response)

    def profiling(self, method, *args, **kw):
        self.profiler = profile.Profile()
        output = self.profiler.runcall(method, *args, **kw)
        self.profiler.dump_stats(settings.PROFILE_FILE)
        return output

    def render_to_template(self, template, **kw):
        lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS,
                                output_encoding='utf-8',
                                input_encoding='utf-8',
                                default_filters=['decode.utf8'])

        translate = self.get_translate()

        try:
            template = lookup.get_template(template)

            return template.render(url_for=self.reverse_url, _=translate, **kw)
        except Exception, e:
            if settings.DEBUG:
                return exceptions.html_error_template().render()
            else:
                logging.exception("Erro ao renderizar o template!")
                raise e

    def render_to_xml(self, data, request_handler, **kw):
        request_handler.set_header("Content-Type", "text/xml; charset=UTF-8")
        return simplexml.dumps(data)
