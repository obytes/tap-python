from tap.tap_object import TapObject
from tap import six
from tap import util
from tap import error
from urllib.parse import quote_plus
class APIResource(TapObject):

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        instance = cls(id, api_key, **params)
        instance.refresh()
        return instance

    def refresh(self):
        url = self.get_instance_url()
        resp = self.request('get', url)
        self.refresh_from(resp)
        return self

    def get_instance_url(self):
        id = self.get('id')

        if not isinstance(id, six.string_types):
            raise error.InvalidRequestError(
                'could not determine wich url to request : instance %s'
                ' has invalid ID %r, %s ID should be type `str`'
                % (type(self).__name__, type(id), 'id'))

        id = util.utf8(id)
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
        return "/v1/%ss" % (base,)

