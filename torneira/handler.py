# coding: utf-8
from cProfile import Profile

from tornado.web import RequestHandler

from torneira import settings


class TorneiraHandler(RequestHandler):
    _action = None

    def initialize(self, *args, **kwargs):
        self._action = kwargs.get('action')

    def get(self, *args, **kwargs):
        self._process_request(*args, **kwargs)

    def post(self, *args, **kwargs):
        self._process_request(*args, **kwargs)

    def _process_request(self, *args, **kwargs):
        assert self._action, 'You need to specify action data for URL or override get/post/etc methods.'

        method_callable = getattr(self, self._action)
        if hasattr(settings, 'PROFILING') and settings.PROFILING is True:
            response = self._profile_request(method_callable, *args, **kwargs)
        else:
            response = method_callable(*args, **kwargs)
        if response is not None:
            self.write(response)

    def _profile_request(self, method, *args, **kwargs):
        assert hasattr(settings, 'PROFILE_FILE'), "Missing PROFILE_FILE config"
        profiler = Profile()
        output = profiler.runcall(method, *args, **kwargs)
        profiler.dump_stats(settings.PROFILE_FILE)
        return output
