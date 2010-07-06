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

from mox import Mox
from torneira.core import server

def test_can_be_load_server():
	_server = server.TorneiraServer("pidfile", 8080, "project_root", "media_dir")
	assert _server.pidfile == "pidfile"
	assert _server.port == 8080
	assert _server.project_root == "project_root"
	assert _server.media_dir == "media_dir"
