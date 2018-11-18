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
>>> tap.api_key = 'sk_test_XKokBfNWv6FIYuTMg5sLPjhJ'
>>> resp = tap.Customer.create(
...     first_name='first name',
...     last_name='last name',
...     email='customer@gmail.com',
...     currency='usd',
...     nationality='Moroccan'
... )
> /opt/app/tap/util.py(105)convert_to_tap_object()
-> if isinstance(resp, list):

(Pdb) tap_response
<tap.response.ApiResponse instance at 0x7f6b04e55128>

(Pdb) tap_response.body
u'{"id":"cus_Mk452018220Mn541888711","object":"customer","live_mode":false,"created":"1542578436122","currency":"usd","nationality":"Moroccan","first_name":"first name","last_name":"last name","email":"customer@gmail.com"}'
```

