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
import logging
import pickle

from torneira.helper.encoding import smart_unicode, smart_str

import memcache


class MemcachedClass():

    def __init__(self, server, timeout):
        self.server = server
        self.default_timeout = int(timeout)
        self._cache = memcache.Client(self.server)
        logging.debug("Memcached start client %s" % server)

    def add(self, key, value, timeout=0):
        if isinstance(value, unicode):
            value = value.encode('utf-8')

        try:
            return self._cache.add(smart_str(key), value, timeout or self.default_timeout)
        except:
            logging.exception("memcache server desligado!")

    def get(self, key, default=None):
        try:
            val = self._cache.get(smart_str(key))
            if val is None:
                return default
            else:
                if isinstance(val, basestring):
                    return smart_unicode(val)
                else:
                    return val
        except:
            logging.exception("memcache server desligado!")
            return None

    def set(self, key, value, timeout=0):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._cache.set(smart_str(key), value, timeout or self.default_timeout)

    def delete(self, key):
        self._cache.delete(smart_str(key))

    def get_many(self, keys):
        return self._cache.get_multi(map(smart_str, keys))

    def close(self, **kwargs):
        self._cache.disconnect_all()

    def stats(self):
        try:
            return self._cache.get_stats()
        except Exception:
            logging.exception("memcache server desligado!")

    def flush_all(self):
        try:
            self._cache.flush_all()
        except Exception:
            logging.exception("memcache server desligado!")


class RedisClass():
    def __init__(self, master, slave, timeout):
        import redis

        host_master, port_master = master.split(':')
        self._cache_master = redis.Redis(host=host_master, port=int(port_master), db=0)
        host_slave, port_slave = slave.split(':')
        self._cache_slave = redis.Redis(host=host_slave, port=int(port_slave), db=0)
        self.default_timeout = int(timeout)

        logging.debug("Redis master start client %s" % master)
        logging.debug("Redis slave start client %s" % slave)

    def add(self, key, value, timeout=0):
        try:
            val = self._cache_master.getset(smart_str(key), pickle.dumps(value))
            self._cache_master.expire(smart_str(key), timeout or self.default_timeout)
            return val
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def get(self, key, default=None):
        try:
            val = self._cache_slave.get(smart_str(key))
            if val is None:
                return default
            else:
                return pickle.loads(val)
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def set(self, key, value, timeout=0):
        try:
            self._cache_master.set(smart_str(key), pickle.dumps(value))
            self._cache_master.expire(smart_str(key), timeout or self.default_timeout)
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def delete(self, key):
        try:
            self._cache_master.delete(smart_str(key))
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def get_many(self, keys):
        try:
            return self._cache_slave.get_multi(map(smart_str, keys))
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def close(self, **kwargs):
        try:
            self._cache_master.disconnect_all()
            self._cache_slave.disconnect_all()
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def stats(self, server='slave'):
        try:
            if server == 'master':
                return self._cache_master.info()
            else:
                return self._cache_slave.info()
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def flush_all(self):
        self._cache.flushdb()

    def stats_master(self):
        try:
            return self._cache_master.info()
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)

    def stats_slave(self):
        try:
            return self._cache_slave.info()
        except redis.ConnectionError, e:
            logging.exception("ConnectionError %s" % e)


class DummyClass():
    def add(self, key, value, timeout=0):
        pass

    def get(self, key, default=None):
        return None

    def set(self, key, value, timeout=0):
        pass

    def delete(self, key):
        pass

    def get_many(self, keys):
        pass

    def close(self, **kwargs):
        pass

    def flush_all(self):
        pass
