import logging
log = logging.getLogger(__name__)

class Root(object):
    """Root

    The main root object for any API traversal
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
        raise KeyError
