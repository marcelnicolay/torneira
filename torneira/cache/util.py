# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect, re, logging, hashlib
from datetime import datetime
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
    
    cachekey = cachekey.replace("{module}",instance.__module__)
    cachekey = cachekey.replace("{classe}",instance.__class__.__name__)
    cachekey = cachekey.replace("{method}",method)
    
    if hasattr(instance, "id") and instance.id:
        cachekey = cachekey.replace("{instanceid}","%s" % instance.id)
    else:
        cachekey = cachekey.replace("{instanceid}","")

    params = {}
    
    argspected = inspect.getargspec(getattr(instance, method).fn).args
    for arg in argspected:
        if arg != 'self':
            params[arg] = ""

    for name, value in kwarguments.iteritems():
        if value:
            params[name] = value.replace(' ','') if isinstance(value,str) else value
    
    keys = params.keys()
    keys.sort()
    
    cachekey = cachekey.replace("{params}", ",".join(["%s=%s" % (key, params[key]) for key in keys]))
    md5key = hashlib.md5(cachekey).hexdigest()
    
    return md5key, cachekey


def cached_method(fn, *arguments, **kwarguments):

    if len(arguments) == 0 :
#       return fn(*arguments, **kwarguments)
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
    def cached_static_fn(*args, **kw):
        return cached_method(fn, *args, **kw)
    # hack for access decorated function
    cached_static_fn.fn = fn
    
    return cached_static_fn

def cached_timeout(timeout):
    def cached(fn):
        def cached_static_fn(*arguments, **kwarguments):
            fn.timeout = timeout
            return cached_method(fn, *arguments, **kwarguments)

        # hack for access decorated function
        cached_static_fn.fn = fn

        return cached_static_fn
    
    return cached

try:
    from tornado import gen
except ImportError:
    pass
    
def async_cached(timeout=None):
    
    def async_cached_fn(fn):

        @gen.engine
        def async_cached_wrapper(instance, callback, *arguments, **kwarguments):
        
            md5key, key = cache_key(instance, fn.__name__, **kwarguments)

            logging.debug("verificando chave %s no cache no formato md5 %s  " % (key, md5key))
            cache = get_cache()
            result = cache.get(md5key)

            if result is None:
                result = yield gen.Task(fn, instance, *arguments, **kwarguments)
                
                cache.set(md5key, result, timeout)

                logging.debug("SET IN CACHE %s" % result)
            else:
                logging.debug("GET FROM CACHE")

            callback(result)

        # hack for access decorated function
        async_cached_wrapper.fn = fn
        
        return async_cached_wrapper
        
    return async_cached_fn
        
        
'''
    expire decorated method from cache
'''
def expire_key(method, **kw):
    if method.__name__ not in ('cached_static_fn', 'async_cached_wrapper'):
        raise ValueError("Somente metodos decorados com cached, podes ser expirados")

    md5key, key = cache_key(method.im_self or method.im_class(), method.fn.__name__ , **kw)

    cache = get_cache()
    logging.debug("[CACHE][expire] - %s {%s}" % (md5key, key))

    cache.delete(md5key)

'''
    set value as decorated method in cache
'''
def set_key(method, value, **kw):
    if method.__name__ not in ('cached_static_fn', 'async_cached_wrapper'):
        raise ValueError("Somente metodos decorados com cached, podes ser expirados")

    md5key, key = cache_key(method.im_self or method.im_class(), method.fn.__name__ , **kw)

    cache = get_cache()
    logging.debug("[CACHE][set] - %s {%s}" % (md5key, key))

    cache.set(md5key, value)
        
        