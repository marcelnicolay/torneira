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

from sqlalchemy import create_engine
from sqlalchemy.interfaces import ConnectionProxy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.interfaces import SessionExtension
from torneira.core import Singleton
import logging
import time
import settings

class TimerProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        if not settings.DEBUG:
            return execute(cursor, statement, parameters, context)
            
        now = time.time()
        try:
            return execute(cursor, statement, parameters, context)
        finally:
            total = time.time() - now
            logging.debug("Query: %s" % statement)
            logging.debug("Total Time: %f" % total)


class TorneiraSession():
	def __new__(cls, *args, **kwarg):
		if not cls._instance:
			engine = create_engine(settings.DATABASE_ENGINE, pool_size=settings.DATABASE_POOL_SIZE, pool_recycle=300, proxy=TimerProxy())
			cls._session = scoped_session(sessionmaker(autocommit=True, autoflush=False, expire_on_commit=False))
		return cls._session

