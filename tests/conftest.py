import tap
import pytest
from . import tap_vcr


@pytest.fixture
@tap_vcr.use_cassette('success_calls.yaml')
def create_customer():

    def fun():
        data = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "nationality": "Moroccan",
            "currency": "MAD"
        }
        customer = tap.Customer.create(**data)
        return customer
    return fun


@pytest.fixture
@tap_vcr.use_cassette('success_calls.yaml')
def create_token():

    def fun():
        data = {
            "card": {
                "number": 5123450000000008,
                "exp_month": 12,
                "exp_year": 21,
                "cvc": 124,
            }
        }

        token = tap.Token.create(**data)
        return token
    return fun



