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

from tornado import locale
from torneira import settings
from routes.util import url_for

from mako import exceptions
from mako.lookup import *
import simplexml

import simplejson
import logging

class BaseController(object):
    _current_locale = None

    def __init__(self):
        self.setup_locale()

    def define_current_locale(self, locale_code):
        self._current_locale = locale.get(locale_code)

    def setup_locale(self):        
        if not hasattr(settings, 'LOCALE'):
            return
            
        assert settings.LOCALE.has_key('code')
        assert settings.LOCALE.has_key('path')
        assert settings.LOCALE.has_key('domain')

        locale_code = settings.LOCALE['code']
        locale.set_default_locale(locale_code)
        locale.load_gettext_translations(settings.LOCALE['path'],
                                         settings.LOCALE['domain'])
        self.define_current_locale(locale_code)

    def get_translate(self):
        if not self._current_locale:
            return lambda s: s
        else:
            return self._current_locale.translate

    def render_to_template(self, template, **kw):
        lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS,
                                output_encoding='utf-8',
                                input_encoding='utf-8',
                                default_filters=['decode.utf8'])

        translate = self.get_translate()

        try:
            template = lookup.get_template(template)

            return template.render(url_for=url_for, _=translate, **kw)
        except Exception, e:
            if settings.DEBUG:
                return exceptions.html_error_template().render()
            else:
                logging.exception("Erro ao renderizar o template!")
                raise e

    def render_error(self, message="Ops! Ocorreu um erro!", **kw):
        return self.render_to_json({"errors":{"error":{"message": message}}}, **kw)

    def render_success(self, message="Operação realizada com sucesso!", **kw):
        return self.render_to_json({"errors":"", "message":message}, **kw)

    def render_to_json(self, data, request_handler, **kw):
        request_handler.set_header("Content-Type", "application/json; charset=UTF-8")
        return simplejson.dumps(data)

    def render_to_xml(self, data, request_handler, **kw):
        request_handler.set_header("Content-Type", "text/xml; charset=UTF-8")
        return simplexml.dumps(data)
    
def render_to_extension(fn):
    def render_to_extension_fn(self, *args, **kargs):

        response = fn(self, *args, **kargs)
        extension = kargs.get('extension')
        request_handler = kargs.get('request_handler')

        if extension and extension == 'json':
            return self.render_to_json(response, request_handler=request_handler)

        elif extension and extension == 'jsonp':
            request_handler.set_header("Content-Type", "application/javascript; charset=UTF-8")
            callback = kargs.get('callback') if kargs.get('callback') else fn.__name__
            return "%s(%s);" % (callback, simplejson.dumps(response))
        
        elif extension and extension == 'xml':
            return self.render_to_xml(response, request_handler=request_handler)
        
        else:
            return response

    return render_to_extension_fn