# coding: utf-8
import re

from tornado.web import URLSpec
from routes.route import Route


def url(route=None, controller=None, action=None, name=None):

    route = Route(name, route)
    route.makeregexp('')

    regexp = re.sub(r'(?<!\\)\\', '', route.regexp)

    return URLSpec(regexp, controller, dict(action=action), name=name)
