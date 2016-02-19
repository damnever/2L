# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.exceptions import ValidationError


error_codes = {
    1010: 'Unknown reason',
    1011: 'Empty fields',
    1012: 'Username does not exists',
    1013: 'Password wrong',
    1014: 'E-mail is not verified',
    1015: 'Username already exists',
    1016: 'E-mail already exists',
    1017: 'Verification code wrong',
    1018: 'Token wrong',
    1019: 'Topic name already exists',
    1020: 'Post title already exists',
    1021: 'Topic already subscribed',
    1022: 'Topic has not been subscribed',
    1023: 'Post already favorited',
    1024: 'Post has not been favorited',
    1025: 'Can not vote up again',
    1026: 'Can not vote down again',
    1027: 'No vote can be cancel',
    1028: 'Topic is not accepted',
    1029: 'Topic vote time has passed',
    1030: 'No more gold today',
}


def _make_error_class(cls_name, code, reason):
    def __init__(self):
        super(self.__class__, self).__init__(code, reason)
    bases = (ValidationError,)
    attrs = {'__init__': __init__}
    return type(cls_name, bases, attrs)


for code, reason in error_codes.items():
    error = ''.join([w.capitalize() for w in reason.replace('-', '').split()])
    globals()[error] = _make_error_class(error, code, reason)
