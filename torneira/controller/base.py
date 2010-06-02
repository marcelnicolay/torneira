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

from mako import exceptions
from mako.lookup import *

import simplejson
import logging

try:
    import settings
except ImportError, ie:
	from torneira.core import settings_default as settings

class BaseController():
    
    def render_to_template(self, template, **kw):
        lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS, 
                                output_encoding='utf-8', 
                                input_encoding='utf-8',
                                default_filters=['decode.utf8'])
        try:
            template = lookup.get_template(template)
            
            return template.render(**kw)
        except Exception, e:
            if settings.DEBUG:
                return exceptions.html_error_template().render()
            else:
                logging.exception("Erro ao renderizar o template!")
                raise e

    def render_error(self, message="Ops! Ocorreu um erro!"):
        return self.render_to_json({"errors":{"error":{"message": message}}})

    def render_success(self, message="Operação realizada com sucesso!"):
        return self.render_to_json({"errors":"", "message":message})
    
    def render_to_json(self, data):
        self.handler.set_header("Content-Type", "application/json; charset=UTF-8")
        return simplejson.dumps(data)
