# -*- coding: utf-8 -*-
#
# Copyright Marcel Nicolay <marcel.nicolay@gmail.com>
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
__version__ = '0.3.2'

try:
    import settings_local as settings
except ImportError, ie:
    try:
        import settings
    except ImportError, ie:
        class settings(object):
            DEBUG = True
            PROFILING = False
            COOKIE_SECRET = ""

settings = settings
