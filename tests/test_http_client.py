from __future__ import absolute_import, division, print_function

import pytest
from tap.http_client import new_default_http_client, HTTPClient

VALID_API_METHODS = ('get', 'post', 'delete')


class ApiClientTestCase(object):
    REQUEST_LIBRARIES = ['requests']

    @pytest.fixture
    def request_mocks(self, mocker):
        request_mocks = {}
        for lib in self.REQUEST_LIBRARIES:
            request_mocks[lib] = mocker.patch("tap.http_client.%s" % (lib,))
        return request_mocks


class TestRetrySleepTimeDefaultHttpClient(ApiClientTestCase):
    from contextlib import contextmanager

    def assert_sleep_times(self, client, expected):
        until = len(expected)
        actual = list(map(lambda i: client._sleep_time_seconds(i + 1), range(until)))
        assert expected == actual

    @contextmanager
    def mock_max_delay(self, new_value):
        original_value = HTTPClient.MAX_DELAY
        HTTPClient.MAX_DELAY = new_value
        try:
            yield self
        finally:
            HTTPClient.MAX_DELAY = original_value

    def test_sleep_time_exponential_back_off(self):
        client = new_default_http_client()
        client._add_jitter_time = lambda t: t
        with self.mock_max_delay(10):
            self.assert_sleep_times(client, [0.5, 1.0, 2.0, 4.0, 8.0])

    def test_initial_delay_as_minimum(self):
        client = new_default_http_client()
        client._add_jitter_time = lambda t: t * 0.001
        initial_delay = HTTPClient.INITIAL_DELAY
        self.assert_sleep_times(client, [initial_delay] * 5)

    def test_maximum_delay(self):
        client = new_default_http_client()
        client._add_jitter_time = lambda t: t
        max_delay = HTTPClient.MAX_DELAY
        expected = [0.5, 1.0, max_delay, max_delay, max_delay]
        self.assert_sleep_times(client, expected)

    def test_randomness_added(self):
        client = new_default_http_client()
        random_value = 0.8
        client._add_jitter_time = lambda t: t * random_value
        base_value = HTTPClient.INITIAL_DELAY * random_value

        with self.mock_max_delay(10):
            expected = [HTTPClient.INITIAL_DELAY,
                        base_value * 2,
                        base_value * 4,
                        base_value * 8,
                        base_value * 16]
            self.assert_sleep_times(client, expected)

    def test_jitter_has_randomness_but_within_range(self):
        client = new_default_http_client()

        jittered_ones = set(
            map(lambda _: client._add_jitter_time(1), list(range(100)))
        )

        assert len(jittered_ones) > 1
        assert all(0.5 <= val <= 1 for val in jittered_ones)

