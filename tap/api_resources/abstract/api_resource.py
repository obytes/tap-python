from __future__ import absolute_import, division, print_function

import tap
from tap.tap_object import TapObject

try:
    from urllib import quote_plus  # Python 2.X
except ImportError:
    from urllib.parse import quote_plus  # Python 3+


class APIResource(TapObject):

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        instance = cls(id, api_key, **params)
        instance.refresh()
        return instance

    def refresh(self):
        url = self.instance_url()
        resp = self.request('get', url)
        self.refresh_from(resp)
        return self

    def instance_url(self):
        id = self.get('id')

        if not isinstance(id, tap.six.string_types):
            raise tap.error.InvalidRequestError(
                'could not determine wich url to request : instance %s'
                ' has invalid ID %r, %s ID should be type `str`'
                % (type(self).__name__, type(id), 'id'))

        id = tap.util.utf8(id)
        base = self.class_url()
        extn = quote_plus(id)
        return '%s/%s' % (base, extn)

    @classmethod
    def class_url(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'This class is abstract should call this method'
                'from subclass of it')

        base = cls.OBJECT_NAME.replace('.', '/')
        return "/v2/%ss" % (base,)

