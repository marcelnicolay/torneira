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
try:
    import urls
except ImportError, ie:
	logging.warn("Not found urls file, using urls default!")
	import urls_default as urls

class TorneiraDispacther():

	__mapper__ = None
	__controllers__ = None
	
	def __new__(cls,*args, kwars**):
		if not cls._instance:
			cls._instance = __new__(*args, *kwargs)
		return cls._instance
		
	def getMapper(self):
		if not self.__mapper__:
			mapper = Mapper()
	        for name, route, controller, action, module in urls.urls:
    	        mapper.connect(name, route, controller="%s.%s" % (module,controller), action=action)
    	    self.__mapper__ = mapper
		return self.__mapper__
		
	def getController(self, controller):
		if not self.__controllers__:
        	self.__controllers__ = {}
        
		if not controller in self.__controllers__:
		    module, ctrl_name = controller.split(".")
		    ctrl = getattr(__import__("controller.%s" % module, fromlist=[ctrl_name]), ctrl_name)
	        self.__controllers__[controller] = ctrl()
    
	    return self.__controllers__[controller]
		
def url(route=None, controller=None, action="index", name=None, module=None):
    return [name, route, controller, action, module]
