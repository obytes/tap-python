from . import tap_vcr

import tap
from tap.api_resources.card import Card



class TestCard(object):

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_create_card(self, customer_id, new_card_token):

        resp = tap.Customer.create_card(customer_id, **{'source': new_card_token})
        assert isinstance(resp, Card)
        assert resp.object == 'card'
        assert resp.id

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_retrieve_card(self, customer_id, card_id):

        resp = tap.Customer.retrieve_card(customer_id, card_id)
        assert isinstance(resp, Card)
        assert resp.id == card_id

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_list_cards(self, customer_id):

        resp = tap.Customer.list_cards(customer_id)
        assert hasattr(resp, 'data')
        assert isinstance(resp.data, list)

    @tap_vcr.use_cassette('success_calls.yaml')
    def test_delete_card(self, customer_id, card_id):

        resp = tap.Customer.delete_card(customer_id, card_id)
        assert resp.deleted == True

