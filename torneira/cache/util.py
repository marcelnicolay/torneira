# -*- coding: utf-8 -*-
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import functools
import inspect
import logging
import hashlib

from tornado import gen

from torneira.cache.backend import MemcachedClass, DummyClass, RedisClass
from torneira import settings

__cache__ = None


def get_cache():
    global __cache__
    if not __cache__:
        if settings.CACHE_BACKEND == "memcached":
            servers = settings.CACHE_BACKEND_OPTS[settings.CACHE_BACKEND]
            __cache__ = MemcachedClass(servers, settings.CACHE_TIMEOUT)
        elif settings.CACHE_BACKEND == "redis":
            master = settings.CACHE_BACKEND_OPTS[settings.CACHE_BACKEND]["master"]
            slave = settings.CACHE_BACKEND_OPTS[settings.CACHE_BACKEND]["slave"]
            __cache__ = RedisClass(master, slave, settings.CACHE_TIMEOUT)
        else:
            __cache__ = DummyClass()
    return __cache__


def cache_key(instance, method, **kwarguments):
    cachekey = "{module}.{classe}({instanceid}).{method}({params})"

    cachekey = cachekey.replace("{module}", instance.__module__)
    cachekey = cachekey.replace("{classe}", instance.__class__.__name__)
    cachekey = cachekey.replace("{method}", method)

    if hasattr(instance, "get_cache_key"):
        cachekey = cachekey.replace("{instanceid}", str(instance.get_cache_key()))
    elif hasattr(instance, "id") and instance.id:
        cachekey = cachekey.replace("{instanceid}", "%s" % instance.id)
    else:
        cachekey = cachekey.replace("{instanceid}", "")

    params = {}

    argspected = inspect.getargspec(getattr(instance, method))
    for arg in argspected[0]:
        if arg != 'self':
            params[arg] = ""

    for name, value in kwarguments.iteritems():
        if value:
            params[name] = value.replace(' ', '') if isinstance(value, str) else value

    keys = params.keys()
    keys.sort()

    cachekey = cachekey.replace("{params}", ",".join(["%s=%s" % (key, params[key]) for key in keys]))
    md5key = hashlib.md5(cachekey).hexdigest()

    return md5key, cachekey


def cached_method(fn, *arguments, **kwarguments):
    if len(arguments) == 0:
        raise ValueError("Somente metodods de instancia podem ser cacheados")

    md5key, key = cache_key(arguments[0], fn.__name__, **kwarguments)

    logging.debug("verificando chave %s no cache no formato md5 %s  " % (key, md5key))
    cache = get_cache()
    result = cache.get(md5key)

    if result is None:
        result = fn(*arguments, **kwarguments)
        if hasattr(fn, 'timeout'):
            cache.set(md5key, result, fn.timeout)
        else:
            cache.set(md5key, result)

        logging.debug("SET IN CACHE %s" % result)
    else:
        logging.debug("GET FROM CACHE")
    return result


def cached(fn):
    @functools.wraps(fn)
    def cached_static_fn(*args, **kw):
        return cached_method(fn, *args, **kw)
    return cached_static_fn


def cached_timeout(timeout):
    def cached(fn):
        @functools.wraps(fn)
        def cached_static_fn(*arguments, **kwarguments):
            fn.timeout = timeout
            return cached_method(fn, *arguments, **kwarguments)
        return cached_static_fn
    return cached


def async_cached(timeout=None):
    def async_inner(fn):
        @functools.wraps(fn)
        @gen.engine
        def wrapper(self, *args, **kwargs):
            assert 'callback' in kwargs, "Functions decorated with async_cached must have an callback argument"
            callback = kwargs['callback']
            del kwargs['callback']

            md5key, key = cache_key(self, fn.__name__, **kwargs)
            logging.debug("verificando chave %s no cache no formato md5 %s  " % (key, md5key))

            cache = get_cache()
            result = cache.get(md5key)

            if result is not None:
                logging.debug("GET FROM CACHE")
            else:
                result = yield gen.Task(fn, self, *args, **kwargs)
                cache.set(md5key, result, timeout)
                logging.debug("SET IN CACHE %s" % result)

            callback(result)
        return wrapper
    return async_inner


def expire_key(method, **kw):
    '''
    expire decorated method from cache
    '''
    if method.__name__ not in ('cached_static_fn', 'async_cached_wrapper', 'cached'):
        raise ValueError("Somente metodos decorados com cached, podes ser expirados")

    md5key, key = cache_key(method.im_self or method.im_class(), method.fn.__name__, **kw)

    cache = get_cache()
    logging.debug("[CACHE][expire] - %s {%s}" % (md5key, key))

    cache.delete(md5key)
