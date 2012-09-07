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

import functools

from torneira.handler import TorneiraHandler
from torneira.template import MakoMixin

try:
    import json
except ImportError:
    import simplejson as json

# simplexml is optional
try:
    import simplexml
except ImportError:
    simplexml = None

class BaseController(TorneiraHandler, MakoMixin):
    def _process_request(self, *args, **kwargs):
        kwargs['request_handler'] = self
        super(BaseController, self)._process_request(*args, **kwargs)

    def _prepare_arguments_for_kwargs(self):
        # There is a bug in this design: if only one argument is received, we
        # don't know if this needs to be a list or a single value. This
        # implementation assumes that you will want a single value, for
        # compatibility.
        arguments = {}
        for key in self.request.arguments.iterkeys():
            values = self.get_arguments(key)
            arguments[key] = values[0] if len(values) == 1 else values

        return arguments

    def get(self, *args, **kwargs):
        kwargs.update(self._prepare_arguments_for_kwargs())
        super(BaseController, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs.update(self._prepare_arguments_for_kwargs())
        super(BaseController, self).post(*args, **kwargs)

    def render_to_json(self, data, request_handler=None, **kwargs):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return json.dumps(data)

    def render_to_xml(self, data, request_handler=None, **kw):
        assert simplexml, "Module simplexml needs to be installed to use this method"
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        return simplexml.dumps(data)

    def render_error(self, message="Ops! Ocorreu um erro!", **kw):
        return self.render_to_json({"errors": {"error": {"message": message}}}, **kw)

    def render_success(self, message="Operação realizada com sucesso!", **kw):
        return self.render_to_json({"errors": "", "message": message}, **kw)


def render_to_extension(fn):
    @functools.wraps(fn)
    def wrapped(self, *args, **kwargs):
        response = fn(self, *args, **kwargs)

        extension = kwargs.get('extension')
        if not extension:
            return response

        if extension == 'json':
            return self.render_to_json(response, request_handler=self)
        elif extension == 'jsonp':
            self.set_header("Content-Type", "application/javascript; charset=UTF-8")
            callback = kwargs.get('callback') if kwargs.get('callback') else fn.__name__
            return "%s(%s);" % (callback, json.dumps(response))
        elif extension == 'xml':
            return self.render_to_xml(response, request_handler=self)

    return wrapped
