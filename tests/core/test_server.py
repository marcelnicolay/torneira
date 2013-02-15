# coding: utf-8
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fudge import patch
from fudge.inspector import arg
from tornado.testing import AsyncTestCase

from torneira.core import server

urls = ()


class RunServerTestCase(AsyncTestCase):
    @patch('torneira.core.server.settings',
           'torneira.core.server.IOLoop',
           'torneira.core.server.Application')
    def test_run_server_should_pass_xheaders_to_correct_method(self, settings, IOLoop, Application):
        settings.has_attr(ROOT_URLS='tests.core.test_server')
        PORT = 1234
        XHEADERS = True

        # Just to prevent the test from hanging
        IOLoop.is_a_stub()

        (Application
            .is_callable()
            .with_args(arg.any(), cookie_secret=None, debug=False)
            .returns_fake()
            .expects('listen')
            .with_args(PORT, xheaders=XHEADERS))

        torneira_server = server.TorneiraServer(PORT, '/my_media/', XHEADERS)
        torneira_server.run()
