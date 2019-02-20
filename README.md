# Tap Python Library

The Tap Python library provides convenient access to the Tap API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses which makes it compatible with a wide range of versions of the Tap
API.

inspired from https://github.com/stripe/stripe-python

## Usage

The library needs to be configured with your account's secret key which is
available in your Tap Dashboard. Set `tap.api_key` to its
value:

``` python
>>> import tap
>>>
>>> # tap.api_key = os.environ.get('TAP_SECRET_KEY')
>>> tap.api_key = 'sk_test_XKokBfNWv6FIYuTMg5sLPjhJ'
>>>
>>> resp = tap.Customer.create(
...     first_name='first name',
...     last_name='last name',
...     email='customer@gmail.com',
...     currency='usd',
...     nationality='Moroccan'
... )
>>>
>>> print('Success: %r' % (resp))
Success: <Customer customer id=cus_k9RY2018525q5LP1962511 at 0x7f2a495e5990> JSON: {
  "created": "1542605100879",
  "currency": "usd",
  "email": "customer@gmail.com",
  "first_name": "first name",
  "id": "cus_k9RY2018525q5LP1962511",
  "last_name": "last name",
  "live_mode": false,
  "nationality": "Moroccan",
  "object": "customer",
  "tap_account": null,
  "tap_version": null
}
```


Battle tested in

<img src="https://www.barmej.com/press/logo.png" alt="barmej" width="200"/>
 
