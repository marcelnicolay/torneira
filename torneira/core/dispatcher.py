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
from routes import Mapper
from torneira.core import Singleton
import logging

from torneira import settings

class TorneiraDispatcher(Singleton):

    def __init__(self):
        self._mapper = None
        self._controllers = None
        self._urls = None
        
    def getUrls(self):
        if not self._urls:
            exec("from %s import urls" % settings.ROOT_URLS)
            self._urls = urls
        return self._urls

    def getMapper(self):
        if not self._mapper:
            mapper = Mapper()
            for name, route, controller, action in self.getUrls():
                mapper.connect(name, route, controller=controller, action=action)
            self._mapper = mapper
        return self._mapper

    def getController(self, controller):
        if not self._controllers:
            self._controllers = {}

        ctrl_name = controller.__name__

        if not ctrl_name in self._controllers:
            self._controllers[ctrl_name] = controller()

        return self._controllers[ctrl_name]
        
    def reset(self):
        self._mapper = None
        self._controllers = None
        self._urls = None

def url(route=None, controller=None, action=None, name=None):
    return [name, route, controller, action]
