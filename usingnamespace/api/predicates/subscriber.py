# Set up the subscriber predicates here

class IsAPI(object):
    def __init__(self, is_or_not, config):
        self.is_or_not = is_or_not

    def text(self):
        return 'is API = {}'.format(self.is_or_not)

    phash = text

    def __call__(self, event):
        return event['request'].is_api == self.is_or_not

