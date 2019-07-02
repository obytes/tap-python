import pytest
from . import tap_vcr
import tap


@pytest.fixture
def create_token():

    def fun(card_number, cvc):
        data = {
            "card": {
                "number": card_number,
                "exp_month": 0o5,
                "exp_year": 21,
                "cvc": cvc,
            }
        }

        token = tap.Token.create(**data)
        return token
    return fun


@pytest.fixture
def create_customer():

    def fun():
        data = {
            "first_name": 'test',
            "last_name": 'test',
            "email": 'test@test.com',
            "nationality": "Moroccan",
            "currency": "MAD"
        }

        customer = tap.Customer.create(**data)
        return customer
    return fun


@pytest.fixture
def create_card(create_token):

    def fun(customer_id):
        token = create_token('5123450000000008', '100')

        card = tap.Customer.create_card(customer_id, **{'source': token.id})
        return card
    return fun


@pytest.fixture
def create_charge():

    def fun(customer_id):
        data = {
            "amount": 10,
            "currency": "KWD",
            "customer": {
                "id": customer_id
            },
            "source": {
                "id": "src_all"
            },
            "post": {
                "url": "http://your_website.com/post_url"
            },
            "redirect": {
                "url": "http://your_website.com/redirect_url"
            }
        }

        charge = tap.Charge.create(**data)
        return charge
    return fun

