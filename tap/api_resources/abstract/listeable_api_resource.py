from tap.api_resources.abstract import APIResource
from tap import util
from tap.api_requestor import APIRequestor


class ListeableAPIResource(APIResource):

    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, api_key=None, stripe_version=None, stripe_account=None,
             **params):
        requestor = APIRequestor(api_key,
                                 api_base=cls.api_base(),
                                 api_version=stripe_version,
                                 account=stripe_account)
        url = cls.class_url()
        response, api_key = requestor.request('get', url, params)
        stripe_object = util.convert_to_stripe_object(response, api_key,
                                                      stripe_version,
                                                      stripe_account)
        stripe_object._retrieve_params = params
        return stripe_object
