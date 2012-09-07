from controller.home import HomeController
from tornado.web import url

urls = (
    url(r"/custom/?", HomeController, dict(action='custom')),
    url(r"/json_service/?", HomeController, dict(action='json_service')),
    url(r"/.*", HomeController, dict(action='index')),
)
