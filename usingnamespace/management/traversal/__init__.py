class Root(object):
    """ManagementRoot

    The main root object for any management traversal
    """

    __name__ = None
    __parent__ = None

    def __init__(self, request):
        """Create the default root object

        :request: The Pyramid request object

        """
        self._request = request

    def __getitem__(self, key):
        """Check to see if we can traverse this ..."""

        next_ctx = None

        if key == 'api':
            next_ctx = API()

        if next_ctx is None:
            raise KeyError

        next_ctx.__parent__ = self

        return next_ctx

class API(object):
    """Management allows access to API tickets"""

    __name__ = 'api'
    __parent__ = None

    def __init__(self):
        """Create the API object"""

        pass

    def __getitem__(self, key):
        """Check to see if we can traverse this ..."""

        raise KeyError
