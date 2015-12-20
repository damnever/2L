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
}


for code, reason in error_codes.items():
    error = ''.join([w.capitalize()
            for w in reason.replace('-', '').split() + ['Error']])
    globals()[error] = ValidationError(code, reason)
