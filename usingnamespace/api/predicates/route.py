# Set up the route predicates here


class API(object):
    def __init__(self, domain, config):
        self.domain = domain

    def text(self):
        return 'Is "{}" API domain?'.format(self.domain)

    phash = text

    def __call__(self, context, request):
        return request.domain == self.domain

