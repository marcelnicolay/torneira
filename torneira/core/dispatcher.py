# coding: utf-8
from tornado.web import URLSpec
from routes.route import Route


def url(route=None, controller=None, action=None, name=None):

    route = Route(name, route)
    route.makeregexp('')

    return URLSpec(route.regexp, controller, dict(action=action))
