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

try:
    import settings_local as settings
except ImportError, ie:
    try:
        import settings
    except ImportError, ie:
        import settings_default as settings

class TorneiraDispatcher(Singleton):

    __mapper__ = None
    __controllers__ = None
    __urls__ = None

    def getUrls(self):
        if not self.__urls__:
            exec("from %s import urls" % settings.ROOT_URLS)
            self.__urls__ = urls
        return self.__urls__

    def getMapper(self):
        if not self.__mapper__:
            mapper = Mapper()
            for name, route, controller, action in self.getUrls():
                mapper.connect(name, route, controller=controller, action=action)
            self.__mapper__ = mapper
        return self.__mapper__

    def getController(self, controller):
        if not self.__controllers__:
            self.__controllers__ = {}

	ctrl_name = controller.__name__
	
        if not ctrl_name in self.__controllers__:
            self.__controllers__[ctrl_name] = controller()

        return self.__controllers__[ctrl_name]


def url(route=None, controller=None, action="index", name=None):
    return [name, route, controller, action]
