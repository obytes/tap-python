from __future__ import absolute_import, division, print_function

import tap
from tap.api_resources.abstract.api_resource import APIResource
try:
    from urllib import quote_plus  # Python 2.X
except ImportError:
    from urllib.parse import quote_plus  # Python 3+


class UpdateableAPIResource(APIResource):

    @classmethod
    def _modify(cls, url, api_key=None, tap_version=None,
                tap_account=None, **params):

        requestor = tap.api_requestor.APIRequestor(api_key, api_version=tap_version,
                                               account=tap_account)

        response, api_key = requestor.request('post', url, params)
        return tap.util.convert_to_tap_object(response, api_key, tap_version, tap_account)

    @classmethod
    def modify(cls, sid, **params):
        url = "%s/%s" % (cls.class_url(), quote_plus(tap.util.utf8(sid)))
        return cls._modify(url, **params)

    def save(self, idempotency_key=None):
        updated_params = self.serialize(None)
        headers = tap.util.populate_headers(idempotency_key)

        if updated_params:
            self.refresh_from(self.request('post', self.instance_url(),
                                           updated_params, headers))
        else:
            tap.util.logger.debug("Trying to save already saved object %r", self)
        return self
