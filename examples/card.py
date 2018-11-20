import tap

######################
# Token Creation
######################

data = {
  "card": {
    "number": 5123450000000008,
    "exp_month": 12,
    "exp_year": 21,
    "cvc": 124,
    "name": "test user",
    "address": {
      "country": "Kuwait",
      "line1": "Salmiya, 21",
      "city": "Kuwait city",
      "street": "Salim",
      "avenue": "Gulf"
    }
  },
  "client_ip": "192.168.1.20"
}

resp = tap.Token.create(**data)
print('Success: %r' % (resp))
token_id = resp.id

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

######################
# Card Creation
######################

tap.Customer.create_card(resp.id, **{'source': token_id})
