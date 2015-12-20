# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os
import importlib
import pkgutil


root_pkg = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


def load_module_attrs(pkg_path, func, recursive=False):
    """Get attributes from modules, use ``func`` to filter attributes,
    ``func`` must return a list.
    """
    attrs = list()
    pkg_name = root_pkg + pkg_path.split(root_pkg)[1].replace('/', '.')

    for _, name, ispkg in pkgutil.iter_modules([pkg_path]):
        if ispkg and recursive:
            next_path = os.path.join(pkg_path, name)
            attrs.extend(load_module_attrs(next_path, func, recursive))
            continue

        module = importlib.import_module('.' + name, pkg_name)
        attr = func(module)
        if attr:
            attrs.extend(attr)

    return attrs
