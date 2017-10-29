import logging

from .archive import (  # noqa
    ArchiveYear,
    ArchiveYearMonth,
    ArchiveYearMonthDay,
)

from .entry import (  # noqa
    Entry
)

from .. import models as m

log = logging.getLogger(__name__)

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

    @property
    def curdomain(self):
        return (
            self._request.dbsession.query(m.Domain).
            filter(m.Domain.domain == self._request.domain).
            first()
        )

    @property
    def entries(self):
        if self.curdomain is not None:
            return (
                self._request.dbsession.query(m.Entry).
                filter(m.Entry.site == self.curdomain.site)
            )
        else:
            raise ValueError
