import tap
from tap import error
from tap import http_client
import util
import six
import calendar
import datetime
import time
import uuid
from response import ApiResponse

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from urlparse import urlsplit, urlunsplit
except ImportError:
    from urllib.parse import urlsplit, urlunsplit


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))


def _encode_nested_dict(key, data, fmt='%s[%s]'):
    d = {}
    for subkey, subvalue in six.iteritems(data):
        d[fmt % (key, subkey)] = subvalue
    return d


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _api_encode(data):
    for key, value in six.iteritems(data):
        key = util.utf8(key)
        if value is None:
            continue
        elif hasattr(value, 'stripe_id'):
            yield (key, value.stripe_id)
        elif isinstance(value, list) or isinstance(value, tuple):
            for i, sv in enumerate(value):
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict("%s[%d]" % (key, i), sv)
                    for k, v in _api_encode(subdict):
                        yield (k, v)
                else:
                    yield ("%s[%d]" % (key, i), util.utf8(sv))
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, util.utf8(value))


class APIRequestor(object):

    def __init__(self, key=None, client=None, api_base=None, api_version=None,
                 account=None):
        self.api_base = api_base or tap.api_base
        self.api_key = key
        self.api_version = api_version or tap.api_version
        self.tap_account = account

        from tap import verify_ssl_certs as verify
        from tap import proxy

        self._client = client or tap.default_http_client or \
            http_client.new_default_http_client(
                verify_ssl_certs=verify, proxy=proxy)

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, my_api_key

    def request_raw(self, method, url, params=None, supplied_headers=None):
        """
        Mechanism for issuing an API call
        """

        if self.api_key:
            my_api_key = self.api_key
        else:
            from tap import api_key
            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                'No API key provided. (HINT: set your API key using '
                '"stripe.api_key = <API-KEY>"). You can generate API keys '
                'from the Stripe web interface.  See https://stripe.com/api '
                'for details, or email support@stripe.com if you have any '
                'questions.')

        abs_url = '%s%s' % (self.api_base, url)

        encoded_params = urlencode(list(_api_encode(params or {})))

        # Don't use strict form encoding by changing the square bracket control
        # characters back to their literals. This is fine by the server, and
        # makes these parameter strings easier to read.
        encoded_params = encoded_params.replace('%5B', '[').replace('%5D', ']')

        if method == 'get' or method == 'delete':
            if params:
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == 'post':
            if supplied_headers is not None and \
                    supplied_headers.get("Content-Type") == \
                    "multipart/form-data":

                # TODO: Look into this case later
                pass

                # generator = MultipartDataGenerator()
                # generator.add_params(params or {})
                # post_data = generator.get_post_data()
                # supplied_headers["Content-Type"] = \
                #     "multipart/form-data; boundary=%s" % (generator.boundary,)
                raise error.APIConnectionError(
                    'Multipart is not supported for now ...')
            else:
                post_data = encoded_params
        else:
            raise error.APIConnectionError(
                'Unrecognized HTTP method %r.  This may indicate a bug in the '
                'Stripe bindings.  Please contact support@stripe.com for '
                'assistance.' % (method,))

        headers = self.request_headers(my_api_key, method)
        if supplied_headers is not None:
            for key, value in six.iteritems(supplied_headers):
                headers[key] = value

        util.log_info('Request to Stripe api', method=method, path=abs_url)
        util.log_debug(
            'Post details',
            post_data=encoded_params, api_version=self.api_version)

        rbody, rcode, rheaders = self._client.request_with_retries(
            method, abs_url, headers, post_data)

        util.log_info(
            'Stripe API response', path=abs_url, response_code=rcode)
        util.log_debug('API response body', body=rbody)
        # if 'Request-Id' in rheaders:
        #     util.log_debug('Dashboard link for request',
        #                    link=util.dashboard_link(rheaders['Request-Id']))
        return rbody, rcode, rheaders, my_api_key

    @classmethod
    def request_headers(cls, api_key, method):

        headers = {
            'Authorization': 'Bearer %s' % (api_key,),
        }

        if method == 'post':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers.setdefault('Idempotency-Key', str(uuid.uuid4()))

        return headers

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = ApiResponse(rbody, rcode, rheaders)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)
        if not (200 <= rcode < 300):
            self.handle_error_response(rbody, rcode, resp.data, rheaders)

        return resp

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = resp['error']
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody, rcode, resp)

        err = None

        # OAuth errors are a JSON object where `error` is a string. In
        # contrast, in API errors, `error` is a hash with sub-keys. We use
        # this property to distinguish between OAuth and API errors.
        # if isinstance(error_data, six.string_types):
        #     err = self.specific_oauth_error(
        #         rbody, rcode, resp, rheaders, error_data)

        if err is None:
            return error.APIError(
                error_data.get('message'), rbody, rcode, resp, rheaders)

        raise err