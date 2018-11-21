import pytest
from . import tap_vcr
import tap

@pytest.fixture
def customer_id():
    return 'cus_a9RF20181234r4DR2199711'


@pytest.fixture
def token_id():
    return 'tok_ryzTND5kYZtcKdslWXBujCOF'

@pytest.fixture
def new_card_token():
    return 'tok_baUJjDYkyxnszgXEwuthQCqP'


@pytest.fixture
def card_id():
    return 'card_JEHx97l5kD0i4dgMUoFrvmTZ'


@pytest.fixture
def charge_id():
    return 'ch_r9M420181619h9Q92777704'


@pytest.fixture
def refund_id():
    return 're_o4R92018049Xq2l283504'


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

