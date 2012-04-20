import urllib

from tornado.httpserver import HTTPRequest
from tornado.escape import parse_qs_bytes, native_str
from tornado.web import Application, HTTPError

from torneira.core.server import TorneiraHandler
from torneira import settings


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

    def make_request(self, request, callback=None):
        cookie_secret = settings.COOKIE_SECRET if hasattr(settings, 'COOKIE_SECRET') else None
        application = Application([], cookie_secret=cookie_secret)
        handler = TestingHandler(application, request, callback=callback)

        try:
            handler.process_request(method=request.method)
            if not callback:
                handler.finish()
        except HTTPError, e:
            handler.response.set_code(e.status_code)

        return handler.response

    def get(self, request, callback=None, **kwargs):
        if isinstance(request, str):
            request = self.create_request(uri=request, method='GET', **kwargs)

        return self.make_request(request, callback=callback)

    def post(self, request, data={}, callback=None, **kwargs):
        if isinstance(request, str):
            request = self.create_request(uri=request, method='POST', body=TestingClient.parse_post_data(data), **kwargs)

        return self.make_request(request, callback=callback)

    def put(self, request, data={}, callback=None, **kwargs):
        if isinstance(request, str):
            request = self.create_request(uri=request, method='PUT', body=TestingClient.parse_post_data(data), **kwargs)

        return self.make_request(request, callback=callback)

    def delete(self, request, data={}, callback=None, **kwargs):
        if isinstance(request, str):
            request = self.create_request(uri=request, method='DELETE', body=TestingClient.parse_post_data(data), **kwargs)

        return self.make_request(request, callback=callback)

    @staticmethod
    def parse_post_data(data):
        if isinstance(data, dict):
            data = TestingClient._convert_dict_to_tuple(data)
        return urllib.urlencode(data)

    @staticmethod
    def _convert_dict_to_tuple(data):
        """Converts params dict to tuple

        This allows lists on each value.
        """
        tuples = []
        for key, value in data.iteritems():
            if isinstance(value, list):
                for each_value in value:
                    tuples.append((key, each_value))
            else:
                tuples.append((key, value))
        return tuples


class TestingResponse(object):
    def __init__(self, request_handler):
        self.body = None
        self.code = None
        self._request_handler = request_handler

    def write(self, body):
        self.body = body

    def set_code(self, code):
        self.code = code

    @property
    def headers(self):
        return self._request_handler._headers


class TestingHandler(TorneiraHandler):
    def __init__(self, application, request, callback=None, **kargs):
        self.response = TestingResponse(self)
        self.callback = callback

        del(request.connection)

        super(TestingHandler, self).__init__(application, request)

    def write(self, body):
        self.response.write(body)

    def finish(self):
        self.response.set_code(self.get_status())
        if self.callback:
            self.callback(self.response)
