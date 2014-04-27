from .site import Site

from .... import models as m

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

        try:
            next_ctx = Site(key)
        except ValueError:
            next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            return next_ctx

    def finalise(self, **kw):
        """Gets the list of sites

        :returns: None
        """

        self.sites = m.DBSession.query(m.Site)
