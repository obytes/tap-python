from . import tap_vcr

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


# @tap_vcr.use_cassette('charge/list_charge.yaml')
# def test_list_charge(create_charge, create_customer):
#     customer = create_customer()
#     charge = create_charge(customer.id)
#     resp = tap.Charge.list()
#     assert len(resp.customers) > 0
