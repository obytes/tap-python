from abstract import DeleteableAPIResource
from abstract import UpdateableAPIResource
from abstract import ListeableAPIResource
from abstract import CreateableAPIResource


class Refund(CreateableAPIResource,
               UpdateableAPIResource,
               DeleteableAPIResource,
               ListeableAPIResource):

    OBJECT_NAME = 'refund'
