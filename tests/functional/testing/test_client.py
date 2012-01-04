import unittest2

from torneira import settings
from torneira.testing.client import TestingClient
from torneira.core.server import asynchronous

class TestController(object):

    def should_be_method(self, request_handler):
        return "should be response"

    @asynchronous
    def should_be_async_method(self, request_handler):
        request_handler.write("should be async response")
        request_handler.finish()

    def should_be_method_error(self, request_handler):
        raise(ValueError())

    def should_be_post_method(self, request_handler, should_be_parameter, **kw):
        return "should be response --- " + should_be_parameter

urls = [
    ("name", "/should-be-url", TestController, "should_be_method"),
    ("name", "/should-be-post", TestController, "should_be_post_method"),
    ("name", "/should-be-url-error", TestController, "should_be_method_error"),
    ("name", "/should-be-async-url", TestController, "should_be_async_method")
]

class TestingClientTestCase(unittest2.TestCase):
    
    def test_can_be_create_request(self):
        
        torneira_client = TestingClient()
        request = torneira_client.create_request(uri="/should-be-url", method="GET")
        
        self.assertEquals(request.uri, "/should-be-url")
        self.assertEquals(request.method, "GET")
        
    def test_can_be_make_request_get(self):

        settings.ROOT_URLS = "functional.testing.test_client"
        
        torneira_client = TestingClient()
        
        response = torneira_client.get("/should-be-url")        

        self.assertEquals(response.body, "should be response")
        self.assertEquals(response.code, 200)
        
        settings.ROOT_URLS = ""
        
    def test_can_be_make_request_post(self):

        settings.ROOT_URLS = "functional.testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.post("/should-be-post", {'should_be_parameter': 'ShouldBePostData'})        

        self.assertEquals(response.body, "should be response --- ShouldBePostData")
        self.assertEquals(response.code, 200)

        settings.ROOT_URLS = ""
        
    def test_can_be_make_request_with_404_error(self):

        settings.ROOT_URLS = "functional.testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.get("/should-be-url-unknow")        

        self.assertEquals(response.code, 404)

        settings.ROOT_URLS = ""

    def test_can_be_make_request_with_500_error(self):

        settings.ROOT_URLS = "functional.testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.get("/should-be-url-error")        

        self.assertEquals(response.code, 500)

        settings.ROOT_URLS = ""
        
    def test_can_be_make_async_request(self):

        settings.ROOT_URLS = "functional.testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.get("/should-be-async-url")        

        self.assertEquals(response.body, "should be async response")
        self.assertEquals(response.code, 200)

        settings.ROOT_URLS = ""