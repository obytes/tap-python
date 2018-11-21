from __future__ import absolute_import, division, print_function

from tap.api_resources.abstract.createable_api_resource import CreateableAPIResource
from tap.api_resources.abstract.updateable_api_resource import UpdateableAPIResource
from tap.api_resources.abstract.deleteable_api_resource import DeleteableAPIResource
from tap.api_resources.abstract.listeable_api_resource import ListeableAPIResource

import tap


@tap.api_resources.abstract.nested_resource_class_methods(
    'card',
    operations=['create', 'retrieve', 'delete', 'list']
)
class Customer(CreateableAPIResource,
               UpdateableAPIResource,
               DeleteableAPIResource,
               ListeableAPIResource):

    OBJECT_NAME = 'customer'
