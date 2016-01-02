# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os.path
import types

from app.libs.utils import load_module_attrs


def _filter(module):
    if hasattr(module, 'urls') and isinstance(module.urls, types.ListType):
        return getattr(module, 'urls')


path = os.path.abspath(os.path.dirname(__file__))
urls = load_module_attrs(path, _filter, True)

__all__ = ['urls']
