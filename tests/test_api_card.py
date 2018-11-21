from . import tap_vcr

import tap
from tap.api_resources.card import Card



@tap_vcr.use_cassette('card/create_card.yaml')
def test_create_card(create_token, create_customer):
    token = create_token('4508750015741019', '100')
    customer = create_customer()

    resp = tap.Customer.create_card(customer.id, **{'source': token.id})
    assert isinstance(resp, Card)
    assert resp.object == 'card'
    assert resp.id


@tap_vcr.use_cassette('card/retrieve_card.yaml')
def test_retrieve_card(create_customer, create_card):
    customer = create_customer()
    card = create_card(customer.id)

    resp = tap.Customer.retrieve_card(customer.id, card.id)
    assert isinstance(resp, Card)
    assert resp.id == card.id

@tap_vcr.use_cassette('card/list_card.yaml')
def test_list_cards(create_customer, create_card):
    customer = create_customer()
    card = create_card(customer.id)

    resp = tap.Customer.list_cards(customer.id)
    assert hasattr(resp, 'data')
    assert isinstance(resp.data, list)
    assert len(resp.data) == 1


@tap_vcr.use_cassette('card/delete_card.yaml')
def test_delete_card(create_customer, create_card):
    customer = create_customer()
    card = create_card(customer.id)

    resp = tap.Customer.delete_card(customer.id, card.id)
    assert resp.deleted
