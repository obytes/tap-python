from . import tap_vcr

import tap
from tap.api_resources.token import Token


@tap_vcr.use_cassette('token/success_calls.yaml')
def test_create_token():
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


@tap_vcr.use_cassette('token/success_calls.yaml')
def test_get_token(create_token):
    token = create_token('5123450000000008', '100')

    token = tap.Token.retrieve(token.id)
    assert isinstance(token, Token)
    assert token.id == token.id
