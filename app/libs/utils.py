# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import re
import os
import base64
import uuid
import importlib
import pkgutil
import hashlib

from app.settings import ROOT_DIR


_AT_RE = re.compile(r'@(?P<name>[^ ,\.;:!\?"\':]+)', re.M | re.S)


def load_module_attrs(pkg_path, func, recursive=False):
    """Get attributes from modules, use ``func`` to filter attributes,
    ``func`` must return a list.
    """
    attrs = list()
    root_pkg = os.path.basename(ROOT_DIR)
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


def encrypt_password(password):
    """Yes, I do know what I am thinking..."""
    mid = ''.join([hex(ord(w))[2:] for w in password])
    return hashlib.sha1(mid).hexdigest()


def gen_token():
    uuid4bytes = lambda: uuid.uuid4().bytes
    return base64.b64encode(uuid4bytes() + uuid4bytes())


def at_content(content, url='/user/'):
    """Find all users and convert @someone to [@someone](<url>someone)."""
    users = _AT_RE.findall(content)
    val = _AT_RE.sub(r'[@\1]({0}\1)'.format(url), content)
    return users, val
