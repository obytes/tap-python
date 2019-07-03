from .abstract import ListeableAPIResource
from .abstract import UpdateableAPIResource
from .abstract import CreateableAPIResource


class Charge(CreateableAPIResource,
             UpdateableAPIResource,
             ListeableAPIResource):

    OBJECT_NAME = 'charge'
