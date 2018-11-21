from . import tap_vcr

import tap
from tap.api_resources.token import Token


class TestToken(object):

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_create_token(self):
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
        token = create_token()

        token = tap.Token.retrieve(token.id)
        assert isinstance(token, Token)
        assert token.id == token.id
