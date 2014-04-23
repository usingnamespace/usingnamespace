# Set up the subscriber predicates here

class IsManagement(object):
    def __init__(self, is_or_not, config):
        self.is_or_not = is_or_not

    def text(self):
        return 'is management = {}'.format(self.is_or_not)

    phash = text

    def __call__(self, event):
        return event['request'].is_management == self.is_or_not
