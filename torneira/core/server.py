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
        cookie_secret = settings.COOKIE_SECRET if hasattr(settings, 'COOKIE_SECRET') else None
        debug = getattr(settings, 'DEBUG', False)

        static_url = URLSpec(r"/media/(.*)", StaticFileHandler, {"path": self.media_dir}),
        urls = static_url + self.urls
        application = Application(urls, cookie_secret=cookie_secret,
                                  debug=debug, xheaders=self.xheaders)

        application.listen(self.port)

        logging.info("Starting Torneira Server on port %s" % self.port)

        IOLoop.instance().start()
