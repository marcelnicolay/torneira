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

from tornado.web import Application, StaticFileHandler, URLSpec
from tornado.ioloop import IOLoop

from torneira import settings


class TorneiraServer(object):

    def __init__(self, port, media_dir, xheaders=False):
        self.port = port
        self.media_dir = media_dir
        self.xheaders = xheaders
        self.urls = self._get_urls()

    def _get_urls(self):
        _imported = __import__(settings.ROOT_URLS, globals(), locals(), ['urls'], -1)
        return _imported.urls

    def run(self):
        conf = {
            'debug': getattr(settings, 'DEBUG', False),
            'cookie_secret': getattr(settings, 'COOKIE_SECRET', None),
        }

        if hasattr(settings, 'LOG_FUNCTION'):
            conf['log_function'] = settings.LOG_FUNCTION

        static_url = URLSpec(r"/media/(.*)", StaticFileHandler, {"path": self.media_dir}),
        urls = static_url + self.urls
        application = Application(urls, **conf)

        application.listen(self.port, xheaders=self.xheaders)

        logging.info("Starting Torneira Server on port %s" % self.port)

        IOLoop.instance().start()
