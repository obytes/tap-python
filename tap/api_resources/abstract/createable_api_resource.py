from tap.api_resources.abstract import APIResource
from tap import util
from tap.api_requestor import APIRequestor


class CreateableAPIResource(APIResource):


    @classmethod
    def create(cls, api_key=None, idempotency_key=None,
               stripe_version=None, stripe_account=None, **params):

        requestor = APIRequestor(api_key,
                                 api_version=stripe_version,
                                 account=stripe_account)
        url = cls.class_url()
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request('post', url, params, headers)

        return util.convert_to_stripe_object(response, api_key, stripe_version,
                                             stripe_account)
