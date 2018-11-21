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
    def test_get_customer(self, customer_id):
        customer = tap.Customer.retrieve(customer_id)
        assert isinstance(customer, Customer)
        assert customer.id == customer_id

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_update_customer(self, customer_id):
        data = {
            "first_name": "new value",
            "last_name": "new value",
            "email": "test@test.com",
            "nationality": "Moroccan",
            "currency": "MAD"
        }

        customer = tap.Customer.modify(customer_id, **data)
        assert isinstance(customer, Customer)
        assert customer.email == data['email']
        assert customer.first_name == data['first_name']
        assert customer.nationality == data['nationality']

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_delete_customer(self, customer_id):
        data = {
            "id": customer_id
        }

        customer = tap.Customer.modify(customer_id, **data)
        resp = customer.delete(**{'id': customer_id})
        assert resp.id == customer.id
        assert resp.deleted

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_list_customers(self):
        resp = tap.Customer.list()
        assert len(resp.customers) > 0
