from . import tap_vcr

import tap
from tap.api_resources.customer import Customer


@tap_vcr.use_cassette('customer/success_calls.yaml')
def test_create_customer():
    data = {
        "first_name": "test",
        "last_name": "test",
        "email": "test@test.com",
        "nationality": "Moroccan",
        "currency": "MAD"
    }
    customer = tap.Customer.create(**data)
    assert isinstance(customer, Customer)
    assert customer.email == data['email']
    assert customer.first_name == data['first_name']
    assert customer.nationality == data['nationality']


@tap_vcr.use_cassette('customer/success_calls.yaml')
def test_get_customer(create_customer):
    customer = create_customer()
    customer = tap.Customer.retrieve(customer.id)
    assert isinstance(customer, Customer)
    assert customer.id == customer.id


@tap_vcr.use_cassette('customer/success_calls.yaml')
def test_update_customer(create_customer):
    customer = create_customer()

    data = {
        "first_name": "new value",
        "last_name": "new value",
        "email": "test@test.com",
        "nationality": "Moroccan",
        "currency": "MAD"
    }

    customer = tap.Customer.modify(customer.id, **data)
    assert isinstance(customer, Customer)
    assert customer.email == data['email']
    assert customer.first_name == data['first_name']
    assert customer.nationality == data['nationality']


@tap_vcr.use_cassette('customer/success_calls.yaml')
def test_delete_customer(create_customer):
    customer = create_customer()

    data = {
        "id": customer.id
    }

    customer = tap.Customer.modify(customer.id, **data)
    resp = customer.delete(**{'id': customer.id})
    assert resp.id == customer.id
    assert resp.deleted


@tap_vcr.use_cassette('customer/success_calls.yaml')
def test_list_customers():
    resp = tap.Customer.list()
    assert len(resp.customers) > 0
