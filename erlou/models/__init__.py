# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os
import inspect

from ..utils import load_module_attrs
from .base import Model, Base, Roles


def _filter(module):
    if module.__name__ == 'base':
        return
    return [v for k, v in module.__dict__.items()
            if inspect.isclass(v) and issubclass(v, Model)]

path = os.path.abspath(os.path.dirname(__file__))
model_classes = load_module_attrs(path, _filter)
models = {model.__name__: model for model in model_classes}

globals().update(models)

__all__ = models.keys() + ['Base', 'Roles']

