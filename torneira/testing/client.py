from tornado.httpserver import HTTPRequest
from tornado.escape import parse_qs_bytes, native_str
from tornado.web import Application, HTTPError

from torneira.core.server import TorneiraHandler
from torneira import settings

import urllib

class TestingClient(object):
    
    def create_request(self, uri, method="GET", headers={}, body=None, remote_ip=None):
        request = HTTPRequest(uri=uri, method=method, headers=headers, body=body, remote_ip=remote_ip)
        
        if body:
            arguments = parse_qs_bytes(native_str(body))
            for name, values in arguments.iteritems():
                values = [v for v in values if v]
                if values:
                    request.arguments.setdefault(name, []).extend(values)
                        
        return request
    
    def make_request(self, request):
        
        cookie_secret = settings.COOKIE_SECRET if hasattr(settings, 'COOKIE_SECRET') else None
        application = Application([], cookie_secret=cookie_secret)
        
        handler = TestingHandler(application, request)

        try:
            handler.process_request(method=request.method)
            handler.finish()
            
        except HTTPError, e:
            handler.response.set_code(e.status_code)
        
        return handler.response
        
    def get(self, request, **kwargs):
        if isinstance(request, str):
            request = self.create_request(uri=request, method='GET', **kwargs)

        return self.make_request(request)
        
    def post(self, request, data={}, **kwargs):
        
        if isinstance(request, str):
            request = self.create_request(uri=request, method='POST', body=urllib.urlencode(data), **kwargs)
            
        return self.make_request(request)
        

class TestingResponse(object):
    
    def __init__(self):
        self.body = None
        self.code = None
        
    def write(self, body):
        self.body = body
        
    def set_code(self, code):
        self.code = code
        
class TestingHandler(TorneiraHandler):
    
    def __init__(self, application, request, **kargs):
        
        self.response = TestingResponse()
        
        del(request.connection)
        
        super(TestingHandler, self).__init__(application, request)
        
    def write(self, body):
        self.response.write(body)
        
    def finish(self):
        self.response.set_code(200)