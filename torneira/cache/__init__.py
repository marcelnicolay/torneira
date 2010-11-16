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