from controller.home import HomeController
from tornado.web import url

urls = (
    url(r"/custom/?", HomeController, dict(action='custom')),
    url(r"/.*", HomeController),
)
