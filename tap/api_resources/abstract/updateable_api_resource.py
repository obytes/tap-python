from tap.api_resources.abstract import APIResource
from tap import util
from tap.api_requestor import APIRequestor
from urllib.parse import quote_plus


class UpdateableAPIResource(APIResource):

    @classmethod
    def _modify(cls, url, api_key=None, idempotency_key=None,
                stripe_version=None, stripe_account=None, **params):
        requestor = APIRequestor(api_key,
                                 api_version=stripe_version,
                                 account=stripe_account)

        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request('post', url, params, headers)
        return util.convert_to_stripe_object(response, api_key, stripe_version,
                                             stripe_account)

    @classmethod
    def modify(cls, sid, **params):
        url = "%s/%s" % (cls.class_url(), quote_plus(util.utf8(sid)))
        return cls._modify(url, **params)

    def save(self, idempotency_key=None):
        updated_params = self.serialize(None)
        headers = util.populate_headers(idempotency_key)

        if updated_params:
            self.refresh_from(self.request('post', self.instance_url(),
                                           updated_params, headers))
        else:
            util.logger.debug("Trying to save already saved object %r", self)
        return self
