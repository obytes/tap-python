api_key = 'sk_test_XKokBfNWv6FIYuTMg5sLPjhJ'
client_id = None
api_base = 'https://api.tap.company'
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
app_info = None
max_network_retries = 0

# Set to either 'debug' or 'info', controls console logging
log = None


from api_resources.customer import Customer
from api_resources.token import Token
from api_resources.charge import Charge
from api_resources.card import Card


from tap.api_resources import *  # noqa
