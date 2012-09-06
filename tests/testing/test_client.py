# coding: utf-8
from tornado.web import asynchronous
from torneira import settings
from torneira.core.server import TorneiraHandler
from torneira.testing.testcase import TestCase


class TestController(TorneiraHandler):

    def should_be_method(self):
        return "should be response"

    @asynchronous
    def should_be_async_method(self):
        self.write("should be async response")
        self.finish()

    def should_respect_status_code(self):
        self.set_status(201)

    def should_be_method_error(self):
        raise(ValueError())

    def should_be_post_method(self, should_be_parameter, **kw):
        return "should be response --- " + should_be_parameter

urls = [
    ("/should-be-url", TestController, dict(action="should_be_method")),
    ("/should-be-post", TestController, dict(action="should_be_post_method")),
    ("/should-be-url-error", TestController, dict(action="should_be_method_error")),
    ("/should-be-async-url", TestController, dict(action="should_be_async_method")),
    ("/should-respect-status-code", TestController, dict(action="should_respect_status_code"))
]
settings.ROOT_URLS = "testing.test_client"


class TestingClientTestCase(TestCase):
    def test_can_be_create_request(self):
        return
        torneira_client = TestingClient()
        request = torneira_client.create_request(uri="/should-be-url", method="GET")
        
        self.assertEquals(request.uri, "/should-be-url")
        self.assertEquals(request.method, "GET")

    def test_can_be_make_request_get(self):

        response = self.fetch("/should-be-url")

        self.assertEquals(response.body, "should be response")
        self.assertEquals(response.code, 200)

    def test_can_be_make_request_put(self):
        return
        settings.ROOT_URLS = "testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.put("/should-be-url")        

        self.assertEquals(response.body, "should be response")
        self.assertEquals(response.code, 200)

        settings.ROOT_URLS = ""

    def test_can_be_make_request_delete(self):
        return
        settings.ROOT_URLS = "testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.delete("/should-be-url")        

        self.assertEquals(response.body, "should be response")
        self.assertEquals(response.code, 200)

        settings.ROOT_URLS = ""
        
    def test_can_be_make_request_post(self):
        return
        settings.ROOT_URLS = "testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.post("/should-be-post", {'should_be_parameter': 'ShouldBePostData'})        

        self.assertEquals(response.body, "should be response --- ShouldBePostData")
        self.assertEquals(response.code, 200)

        settings.ROOT_URLS = ""

    def test_can_be_make_request_with_404_error(self):
        return
        settings.ROOT_URLS = "testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.get("/should-be-url-unknow")        

        self.assertEquals(response.code, 404)

        settings.ROOT_URLS = ""

    def test_can_be_make_request_with_500_error(self):
        return
        settings.ROOT_URLS = "testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.get("/should-be-url-error")        

        self.assertEquals(response.code, 500)

        settings.ROOT_URLS = ""
        
    def test_can_be_make_async_request(self):
        return
        settings.ROOT_URLS = "testing.test_client"

        torneira_client = TestingClient()

        response = torneira_client.get("/should-be-async-url")        

        self.assertEquals(response.body, "should be async response")
        self.assertEquals(response.code, 200)

        settings.ROOT_URLS = ""

    def test_should_respect_status_code(self):
        return
        settings.ROOT_URLS = "testing.test_client"
        client = TestingClient()
        response = client.get('/should-respect-status-code')

        self.assertEquals(response.code, 201)
        settings.ROOT_URLS = ""
