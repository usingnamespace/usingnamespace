import logging
log = logging.getLogger(__name__)

from .v1 import Root as v1Root

class Root(object):
    """Root

    The main root object for v1 API traversal
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

        if key == 'v1':
            next_ctx = v1Root(self._request)

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            return next_ctx
