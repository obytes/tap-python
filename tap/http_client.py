from __future__ import absolute_import, division, print_function

import os
import sys
import textwrap
import time
import random
from tap import error, util

try:
    import requests
except ImportError:
    requests = None
else:
    try:
        # Require version 0.8.8, but don't want to depend on distutils
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split('.')]
    except Exception:
        # Probably some new-fangled version, so it should support verify
        pass
    else:
        if (major, minor, patch) < (0, 8, 8):
            sys.stderr.write(
                'Warning: the Tap library requires that your Python '
                '"requests" library be newer than version 0.8.8, but your '
                '"requests" library is version %s. Tap will fall back to '
                'an alternate HTTP library so everything should work. We '
                'recommend upgrading your "requests" library. If you have any '
                'questions, please contact support@tap.com. (HINT: running '
                '"pip install -U requests" should upgrade your requests '
                'library to the latest version.)' % (version,))
            requests = None


def new_default_http_client(*args, **kwargs):
    return RequestsClient(*args, **kwargs)


class HTTPClient(object):
    MAX_DELAY = 2
    INITIAL_DELAY = 0.5

    def __init__(self, verify_ssl_certs=True, proxy=None):
        self._verify_ssl_certs = verify_ssl_certs
        if proxy:
            if type(proxy) is str:
                proxy = {"http": proxy, "https": proxy}
            if not (type(proxy) is dict):
                raise ValueError(
                    "Proxy(ies) must be specified as either a string "
                    "URL or a dict() with string URL under the"
                    " ""https"" and/or ""http"" keys.")
        self._proxy = proxy.copy() if proxy else None

    def request_with_retries(self, method, url, headers, post_data=None):
        num_retries = 0

        while True:
            try:
                num_retries += 1
                response = self.request(method, url, headers, post_data)
                connection_error = None
            except error.APIConnectionError as e:
                connection_error = e
                response = None

            if self._should_retry(response, connection_error, num_retries):
                if connection_error:
                    util.log_info("Encountered a retryable error %s" %
                                  connection_error.user_message)

                sleep_time = self._sleep_time_seconds(num_retries)
                util.log_info(("Initiating retry %i for request %s %s after "
                               "sleeping %.2f seconds." %
                               (num_retries, method, url, sleep_time)))
                time.sleep(sleep_time)
            else:
                if response is not None:
                    return response
                else:
                    raise connection_error

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError(
            'HTTPClient subclasses must implement `request`')

    def _should_retry(self, response, api_connection_error, num_retries):
        if response is not None:
            _, status_code, _ = response
            should_retry = status_code == 409
        else:
            # We generally want to retry on timeout and connection
            # exceptions, but defer this decision to underlying subclass
            # implementations. They should evaluate the driver-specific
            # errors worthy of retries, and set flag on the error returned.
            should_retry = api_connection_error.should_retry
        return should_retry and num_retries < self._max_network_retries()

    def _max_network_retries(self):
        from tap import max_network_retries
        # Configured retries, isolated here for tests
        return max_network_retries

    def _sleep_time_seconds(self, num_retries):
        # Apply exponential backoff with initial_network_retry_delay on the
        # number of num_retries so far as inputs.
        # Do not allow the number to exceed max_network_retry_delay.
        sleep_seconds = min(
            HTTPClient.INITIAL_DELAY * (2 ** (num_retries - 1)),
            HTTPClient.MAX_DELAY)

        sleep_seconds = self._add_jitter_time(sleep_seconds)

        # But never sleep less than the base sleep seconds.
        sleep_seconds = max(HTTPClient.INITIAL_DELAY, sleep_seconds)
        return sleep_seconds

    def _add_jitter_time(self, sleep_seconds):
        # Randomize the value in [(sleep_seconds/ 2) to (sleep_seconds)]
        # Also separated method here to isolate randomness for tests
        sleep_seconds *= (0.5 * (1 + random.uniform(0, 1)))
        return sleep_seconds

    def close(self):
        raise NotImplementedError(
            'HTTPClient subclasses must implement `close`')


class RequestsClient(HTTPClient):
    name = 'requests'

    def __init__(self, timeout=80, session=None, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)
        self._timeout = timeout
        self._session = session or requests.Session()

    def request(self, method, url, headers, post_data=None):
        kwargs = {}
        if self._verify_ssl_certs:
            kwargs['verify'] = os.path.join(
                os.path.dirname(__file__), 'data/ca-certificates.crt')
        else:
            kwargs['verify'] = False

        if self._proxy:
            kwargs['proxies'] = self._proxy

        try:
            try:
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               data=post_data,
                                               timeout=self._timeout,
                                               **kwargs)
            except TypeError as e:
                raise TypeError(
                    'Warning: It looks like your installed version of the '
                    '"requests" library is not compatible with Tap\'s '
                    'usage thereof. (HINT: The most likely cause is that '
                    'your "requests" library is out of date. You can fix '
                    'that by running "pip install -U requests".) The '
                    'underlying error was: %s' % (e,))

            # This causes the content to actually be read, which could cause
            # e.g. a socket timeout. TODO: The other fetch methods probably
            # are susceptible to the same and should be updated.
            content = result.content
            status_code = result.status_code
        except Exception as e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self._handle_request_error(e)
        return content, status_code, result.headers

    def _handle_request_error(self, e):

        # Catch SSL error first as it belongs to ConnectionError,
        # but we don't want to retry
        if isinstance(e, requests.exceptions.SSLError):
            msg = ("Could not verify Tap's SSL certificate.  Please make "
                   "sure that your network is not intercepting certificates.  "
                   "If this problem persists, let us know at "
                   "support@tap.com.")
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False
        # Retry only timeout and connect errors; similar to urllib3 Retry
        elif isinstance(e, requests.exceptions.Timeout) or \
                isinstance(e, requests.exceptions.ConnectionError):
            msg = ("Unexpected error communicating with Tap.  "
                   "If this problem persists, let us know at "
                   "support@tap.com.")
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = True
        # Catch remaining request exceptions
        elif isinstance(e, requests.exceptions.RequestException):
            msg = ("Unexpected error communicating with Tap.  "
                   "If this problem persists, let us know at "
                   "support@tap.com.")
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False
        else:
            msg = ("Unexpected error communicating with Tap. "
                   "It looks like there's probably a configuration "
                   "issue locally.  If this problem persists, let us "
                   "know at support@tap.com.")
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
            should_retry = False

        msg = textwrap.fill(msg) + "\n\n(Network error: %s)" % (err,)
        raise error.APIConnectionError(msg, should_retry=should_retry)

    def close(self):
        if self._session is not None:
            print("closing!")
            self._session.close()
