from __future__ import absolute_import, division, print_function

import os

import tap


tap.api_key = os.environ.get('TAP_SECRET_KEY')

print("Attempting charge...")

resp = tap.Customer.create(
    first_name='first name',
    last_name='last name',
    email='customer@gmail.com',
    currency='usd',
    nationality='Moroccan'
)

print('Success: %r' % (resp))
