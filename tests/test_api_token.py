from . import tap_vcr

import tap
from tap.api_resources.token import Token


class TestCustomer(object):

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_create_customer(self):
        data = {
            "card": {
                "number": 5123450000000008,
                "exp_month": 12,
                "exp_year": 21,
                "cvc": 124,
            }
        }

        token = tap.Token.create(**data)
        assert isinstance(token, Token)
        assert token.object == 'token'
        assert token.type == 'CARD'

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_get_token(self, create_token):
        _token = create_token()
        token = tap.Token.retrieve(_token.id)
        assert isinstance(token, Token)
        assert token.id == _token.id
