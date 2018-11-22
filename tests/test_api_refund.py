from . import tap_vcr
import pytest
import tap
from tap.api_resources.refund import Refund


@pytest.mark.xfail(reason='Not sure why')
@tap_vcr.use_cassette('refund/create_refund.yaml')
def test_create_refund(create_customer, create_charge):
    customer = create_customer()
    charge = create_charge(customer.id)

    data = {
        "charge_id": charge.id,
        "amount": charge.amount,
        "currency": "KWD",
        "description": "Test Description",
        "reason": "requested_by_customer"
    }

    refund = tap.Refund.create(**data)
    assert isinstance(refund, Refund)
    assert charge.object == 'refund'
