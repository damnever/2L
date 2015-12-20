# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from abc import ABCMeta, abstractmethod

from six import with_metaclass


class LRU(with_metaclass(ABCMeta, object)):
    """Make ensure the methods you overrided is FIFO."""

    def __init__(self, capacity):
        self._capacity = capacity

    @abstractmethod
    def has_key(self, key):
        return False

    @abstractmethod
    def add_key_value(self, key, value):
        pass

    @abstractmethod
    def get_by_key(self, key, default=None):
        return default

    @abstractmethod
    def pop_key_value(self):
        return None, None

    @abstractmethod
    def pop_by_key(self, key):
        return None

    @abstractmethod
    def count(self):
        return 0

    def set_cache(self, key, value):
        if self.has_key(key):
            self.pop_by_key(key)
        elif self.count() >= self._capacity:
            self.pop_key_value()
        self.add_key_value(key, value)

    def get_cache(self, key):
        if self.has_key(key):
            value = self.pop_by_key(key)
            self.set_cache(key, value)
            return value
        return self.get_by_key(key)

    @classmethod
    def __subclasshook__(cls, C):
        def _has_methods(d):
            for method in ('has_key', 'add_key_value', 'get_by_key',
                           'pop_by_key', 'pop_key_value'):
                if method not in d:
                    return False
            return True
        if cls is LRU:
            if any(_has_methods(B.__dict__) for B in C):
                return True
        raise NotImplemented
