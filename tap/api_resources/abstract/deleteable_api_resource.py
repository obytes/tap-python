from tap.api_resources.abstract.api_resource import APIResource


class DeleteableAPIResource(APIResource):

    def delete(self, **params):
        self.refresh_from(self.request('delete', self.instance_url(), params))
        return self
