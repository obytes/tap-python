from __future__ import absolute_import, division, print_function

from tap.api_resources.abstract.api_resource import APIResource
from tap import api_requestor, util


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, api_key=None, tap_version=None, tap_account=None, **params):

        requestor = api_requestor.APIRequestor(api_key, api_version=tap_version,
                                               account=tap_account)

        url = cls.class_url()
        resp, api_key = requestor.request('post', url, params)

        return util.convert_to_tap_object(resp, api_key, tap_version, tap_account)
