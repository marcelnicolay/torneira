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

try:
    import json
except ImportError:
    import simplejson as json


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
            return "%s(%s);" % (callback, json.dumps(response))
        
        elif extension and extension == 'xml':
            return self.render_to_xml(response, request_handler=request_handler)
        
        else:
            return response

    return render_to_extension_fn
