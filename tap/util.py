from __future__ import absolute_import, division, print_function

import logging
import sys
import os
import re
import tap
from tap import six


TAP_LOG = os.environ.get('TAP_LOG')
logger = logging.getLogger(__name__)


def _console_log_level():
    if tap.log in ['debug', 'info']:
        return tap.log
    elif TAP_LOG in ['debug', 'info']:
        return TAP_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == 'debug':
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ['debug', 'info']:
        print(msg, file=sys.stderr)
    logger.info(msg)


def _test_or_live_environment():
    if tap.api_key is None:
        return
    match = re.match(r'sk_(live|test)_', tap.api_key)
    if match is None:
        return
    return match.groups()[0]


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if six.PY3 and hasattr(val, 'decode'):
            val = val.decode('utf-8')
        # Check if val is already a string to avoid re-encoding into
        # ascii. Since the code is sent through 2to3, we can't just
        # use unicode(val, encoding='utf8') since it will be
        # translated incorrectly.
        if not isinstance(val, six.string_types):
            val = six.text_type(val)
        if re.search(r'\s', val):
            val = repr(val)
        # key should already be a string
        if re.search(r'\s', key):
            key = repr(key)
        return u'{key}={val}'.format(key=key, val=val)
    return u' '.join([fmt(key, val) for key, val in sorted(props.items())])


def utf8(value):
    if six.PY2 and isinstance(value, six.text_type):
        return value.encode('utf-8')
    else:
        return value

