import six
import api_requestor
import util
import json


class TapObject(dict):

    def __init__(self, id=None, api_key=None, tap_version=None,
                 tap_account=None, **params):

        object.__setattr__(self, 'api_key', api_key)
        object.__setattr__(self, 'tap_version', tap_version)
        object.__setattr__(self, 'tap_account', tap_account)
        object.__setattr__(self, 'params', params)

        if id:
            self['id'] = id

        super(TapObject, self).__init__()

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(TapObject, self).__setattr__(k, v)

        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(TapObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(TapObject, self).__setitem__(k, v)

    def __getitem__(self, k):
        try:
            return super(TapObject, self).__getitem__(k)
        except KeyError as err:
            raise err

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), six.string_types):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), six.string_types):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if six.PY2:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return json.dumps(self.to_dict_recursive(), sort_keys=True,
                          indent=2)

    def to_dict(self):
        return dict(self)

    def to_dict_recursive(self):
        d = dict(self)
        for k, v in six.iteritems(d):
            if isinstance(v, TapObject):
                d[k] = v.to_dict_recursive()
        return d

    def request(self, method, url, params=None, headers=None):

        requestor = api_requestor.APIRequestor(
            key=self.api_key, api_version=self.tap_version, account=self.tap_account)

        response, api_key = requestor.request(method, url, params, headers)

        return util.convert_to_tap_object(response, api_key,
                                          self.tap_version,
                                          self.tap_account)

    @classmethod
    def construct_from(cls, values, api_key=None, tap_version=None,
                       tap_account=None):

        instance = cls(values.get('id'), api_key=api_key,
                       stripe_version=tap_version,
                       stripe_account=tap_account)
        instance.refresh_from(values, api_key=api_key,
                              tap_version=tap_version,
                              tap_account=tap_account)
        return instance

    def refresh_from(self, values, api_key=None, tap_version=None,
                     tap_account=None):

        self.api_key = \
            api_key or getattr(values, 'api_key', None)

        self.stripe_version = \
            tap_version or getattr(values, 'tap_version', None)

        self.stripe_account = \
            tap_account or getattr(values, 'tap_account', None)

        for k, v in six.iteritems(values):
            super(TapObject, self).\
                __setitem__(k, util.convert_to_tap_object(v, api_key, tap_version, tap_account))
