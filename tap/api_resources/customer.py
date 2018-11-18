from __future__ import absolute_import, division, print_function

from tap.api_resources.abstract.createable_api_resource import CreateableAPIResource
from tap.api_resources.abstract.updateable_api_resource import UpdateableAPIResource
from tap.api_resources.abstract.deleteable_api_resource import DeleteableAPIResource
from tap.api_resources.abstract.listeable_api_resource import ListeableAPIResource

import tap

class Customer(ListeableAPIResource, CreateableAPIResource,
               UpdateableAPIResource, DeleteableAPIResource):

    OBJECT_NAME = 'customer'

    def delete_discount(self, **params):
        requestor = tap.api_requestor.APIRequestor(self.api_key,
                                               api_version=self.tap_version,
                                               account=self.tap_account)
        url = self.instance_url() + '/discount'
        _, api_key = requestor.request('delete', url, params)
        self.refresh_from({'discount': None}, api_key, True)
