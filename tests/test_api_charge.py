from . import tap_vcr
import pytest
import tap
from tap.api_resources.charge import Charge


@tap_vcr.use_cassette('charge/create_charge.yaml')
def test_create_charge(create_customer):
    customer = create_customer()
    data = {
        "amount": 10,
        "currency": "KWD",
        "customer": {
            "id": customer.id
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
    assert isinstance(charge, Charge)
    assert charge.object == 'charge'


@tap_vcr.use_cassette('charge/retrieve_charge.yaml')
def test_retrieve_charge(create_charge, create_customer):
    customer = create_customer()
    charge = create_charge(customer.id)

    charge = tap.Charge.retrieve(charge.id)
    assert isinstance(charge, Charge)
    assert charge.id == charge.id


@pytest.mark.xfail(reason='Got this from Tap API: Sorry, we couldn\'t achieve your request at the moment. Please try again later, or contact our customer support.')
@tap_vcr.use_cassette('charge/update_charge.yaml')
def test_update_charge(create_charge, create_customer):
    customer = create_customer()
    charge = create_charge(customer.id)

    data = {
      "description": "test",
      "receipt": {
        "email": False,
        "sms": True
      },
      "metadata": {
        "udf2": "test"
      }
    }

    resp = tap.Charge.modify(charge.id, **data)
    assert isinstance(resp, Charge)
    assert resp.amount == data['amount']
    assert resp.currency == data['currency']


@pytest.mark.xfail(reason='Got this from Tap API: Charge not found')
@tap_vcr.use_cassette('charge/list_charge.yaml')
def test_list_charge(create_charge, create_customer):
    customer = create_customer()
    charge = create_charge(customer.id)
    resp = tap.Charge.list()
    assert len(resp.customers) > 0
