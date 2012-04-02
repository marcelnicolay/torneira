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
import datetime

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from torneira.core.meta import TorneiraSession

metadata = MetaData()


class MetaBaseModel(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        return DeclarativeMeta.__init__(cls, classname, bases, dict_)

Model = declarative_base(metadata=metadata, metaclass=MetaBaseModel)


class Repository(object):
    def as_dict(self):
        items = {}
        for attrname in dir(self):
            if attrname.startswith("_"):
                continue

            attr = getattr(self, attrname)
            if isinstance(attr, (basestring, int, float, long)):
                items[attrname] = attr
            if isinstance(attr, (datetime.datetime, datetime.time)):
                items[attrname] = attr.isoformat()
            if isinstance(attr, list):
                items[attrname] = [x.as_dict() for x in attr]

        return items

    @classmethod
    def get(cls, id):
        session = TorneiraSession()
        return session.query(cls).get(id)

    @classmethod
    def fetch_by(cls, **kw):
        session = TorneiraSession()
        return session.query(cls).filter_by(**kw)

    @classmethod
    def all(cls, limit=None):
        session = TorneiraSession()
        if limit:
            return session.query(cls).all()[limit[0]:limit[1]]
        return session.query(cls).all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls()
        for k, v in kwargs.items():
            setattr(instance, k, v)

        instance.save()
        return instance

    def delete(self):
        session = TorneiraSession()
        session.delete(self)
        session.flush()

    def save(self):
        session = TorneiraSession()
        if not self.id:
            session.add(self)
        session.flush()
