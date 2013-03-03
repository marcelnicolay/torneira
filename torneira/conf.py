# coding: utf-8
import os


class EmptySettings(object):
    pass


class LazySettings(object):
    """'Inspired' by Django's LazySettings class"""
    _wrapped = None

    def _import_module(self):
        if not self._wrapped:
            module_name = os.getenv('TORNEIRA_SETTINGS_MODULE', 'settings')
            try:
                self._wrapped = __import__(module_name, globals(), locals(), [], -1)
            except ImportError:
                self._wrapped = EmptySettings()

    def __getattr__(self, name):
        if name == "_wrapped":
            return self.__dict__["_wrapped"]
        else:
            self._import_module()
            return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            self.__dict__["_wrapped"] = value
        else:
            self._import_module()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        self._import_module()
        delattr(self._wrapped, name)


settings = LazySettings()

__all__ = (
    'settings',
)
