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
		
	@staticmethod
	def getMapper():
		if not TorneiraDispacther.__mapper__:
			mapper = Mapper()
	        for name, route, controller, action, module in urls.urls:
    	        mapper.connect(name, route, controller="%s.%s" % (module,controller), action=action)
    	    TorneiraDispacther.__mapper__ = mapper
		return TorneiraDispacther.__mapper__
	
	@staticmethod	
	def getController(self, controller):
		if not TorneiraDispacther.__controllers__:
        	TorneiraDispacther.__controllers__ = {}
        
		if not controller in TorneiraDispacther.__controllers__:
		    module, ctrl_name = controller.split(".")
		    ctrl = getattr(__import__("controller.%s" % module, fromlist=[ctrl_name]), ctrl_name)
	        TorneiraDispacther.__controllers__[controller] = ctrl()
    
	    return TorneiraDispacther.__controllers__[controller]
		
def url(route=None, controller=None, action="index", name=None, module=None):
    return [name, route, controller, action, module]
