from handlers.home import HomeHandler
from tornado.web import url


urls = (
    url(r"/custom/?", HomeHandler, {'action': 'custom'}),
    url(r"/json_service/?", HomeHandler, {'action': 'json_service'}),
    url(r"/.*", HomeHandler, {'action': 'index'}),
)
