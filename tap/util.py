from __future__ import absolute_import, division, print_function

import logging
import sys
import os
import re
import tap
import tap
from tap.response import ApiResponse


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
        if tap.six.PY3 and hasattr(val, 'decode'):
            val = val.decode('utf-8')
        # Check if val is already a string to avoid re-encoding into
        # ascii. Since the code is sent through 2to3, we can't just
        # use unicode(val, encoding='utf8') since it will be
        # translated incorrectly.
        if not isinstance(val, tap.six.string_types):
            val = tap.six.text_type(val)
        if re.search(r'\s', val):
            val = repr(val)
        # key should already be a string
        if re.search(r'\s', key):
            key = repr(key)
        return u'{key}={val}'.format(key=key, val=val)
    return u' '.join([fmt(key, val) for key, val in sorted(props.items())])


def utf8(value):
    if tap.six.PY2 and isinstance(value, tap.six.text_type):
        return value.encode('utf-8')
    else:
        return value


def populate_headers(idempotency_key):
    if idempotency_key is not None:
        return {"Idempotency-Key": idempotency_key}
    return None

OBJECT_CLASSES = {}

def load_classes():
    from tap.api_resources.customer import Customer
    from tap.api_resources.token import Token
    from tap.api_resources.charge import Charge
    from tap.api_resources.refund import Refund

    return {
        Customer.OBJECT_NAME: Customer,
        Token.OBJECT_NAME: Token,
        Charge.OBJECT_NAME: Charge,
        Refund.OBJECT_NAME: Refund
    }


def convert_to_tap_object(resp, api_key=None, tap_version=None,
                          tap_account=None):

    from tap.tap_object import TapObject
    global OBJECT_CLASSES

    if len(OBJECT_CLASSES) == 0:
        OBJECT_CLASSES = load_classes()

    if isinstance(resp, ApiResponse):
        tap_response = resp
        resp = resp.data

    if isinstance(resp, list):
        return [convert_to_tap_object(i, api_key, tap_version,
                                      tap_account) for i in resp]

    elif isinstance(resp, dict) and not isinstance(resp, TapObject):
        klass_name = resp.get('object')
        types = OBJECT_CLASSES.copy()

        if isinstance(klass_name, tap.six.string_types):
            klass = types.get(klass_name, tap.tap_object.TapObject)
        else:
            klass = tap.tap_object.TapObject

        return klass.construct_from(resp, api_key,
                                    tap_version=tap_version,
                                    tap_account=tap_account)
    else:
        return resp
