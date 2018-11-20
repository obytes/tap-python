from __future__ import absolute_import, division, print_function

import tap


# tap.api_key = os.environ.get('TAP_SECRET_KEY')

tap.api_key = 'sk_test_XKokBfNWv6FIYuTMg5sLPjhJ'

######################
# Customer Creation
######################
data = {
  "first_name": "test",
  "last_name": "test",
  "email": "test@test.com",
  "nationality": "Moroccan",
  "currency": "MAD"
}

resp = tap.Customer.create(**data)
print('Success: %r' % (resp))


######################
# Customer Update
######################
data = {
  "first_name": "test",
  "last_name": "test",
  "email": "test@test.com",
  "nationality": "Amirican",
  "currency": "USD"
}

resp = tap.Customer.modify(resp.id, **data)
print('Success: %r' % (resp))

