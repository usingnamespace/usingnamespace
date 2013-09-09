# Package

import logging
log = logging.getLogger(__name__)

from Archive import (
            ArchiveYear,
            ArchiveYearMonth,
            ArchiveYearMonthDay,
        )

from Entry import (
        SingleEntry,
        )

from ..models import (
            DBSession,
            Domain,
            Entry,
        )

class MainRoot(object):
    """The usingnamespace root factory

    This will return the next part in the traversal tree, generally some
    resource.
    """

    __name__ = None
    __parent__ = None
    curdomain = None
    entries = None

    def __init__(self, request):
        """Create the default root object

        :request: The Pyramid request object

        """
        self._request = request

    def __getitem__(self, key):
        """Returns the next item in the traversal.

        :key: The key passed in from the traverser
        :returns: The next resource object down the line

        """

        log.debug("Attempting to get the next: {}".format(key))

        next_ctx = None

        if key == 'tags':
            pass

        if key == 'page':
            pass

        # Last resort, try and see if it is a valid year
        try:
            next_ctx = ArchiveYear(key)
        except ValueError:
            next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            next_ctx._request = self._request
            return next_ctx

    def finalise(self, **kw):
        """Attempts to find out if the domain being used is valid.

        If the domain being used is not a valid domain, we raise ValueError, if
        it is valid we set up self.entries to filter any possible entries
        against the current domains ID.

        :returns: None
        """

        self.curdomain = DBSession.query(Domain) \
                .filter(Domain.domain == self._request.domain) \
                .first()

        if self.curdomain is not None:
            self.entries = DBSession.query(Entry) \
                    .filter(Entry.site == self.curdomain.site)
            return None
        else:
            raise ValueError

class ManagementRoot(object):
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
        raise KeyError
