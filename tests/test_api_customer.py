from . import tap_vcr

import tap
from tap.api_resources.customer import Customer


class TestCustomer(object):

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_create_customer(self):
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

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_get_customer(self, create_customer):
        _customer = create_customer()
        customer = tap.Customer.retrieve(_customer.id)
        assert isinstance(customer, Customer)
        assert customer.email == _customer.email

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_update_customer(self, create_customer):
        _customer = create_customer()
        data = {
            "first_name": "new value",
            "last_name": "new value",
            "email": "test@test.com",
            "nationality": "Moroccan",
            "currency": "MAD"
        }

        customer = tap.Customer.modify(_customer.id, **data)
        assert isinstance(customer, Customer)
        assert customer.email == data['email']
        assert customer.first_name == data['first_name']
        assert customer.nationality == data['nationality']

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_delete_customer(self, create_customer):
        _customer = create_customer()

        resp = _customer.delete(**{'id': _customer.id})
        assert resp.id == _customer.id
        assert resp.deleted

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_list_customers(self):
        resp = tap.Customer.list()
        assert len(resp.customers) > 0
