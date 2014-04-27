from pyramid.view import view_config


class APIHome(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context='..traversal.Root', route_name='api', renderer='json')
    def main(self):
        v1url = self.request.resource_url(self.context, 'v1')
        return {
                'v1': v1url
                }


