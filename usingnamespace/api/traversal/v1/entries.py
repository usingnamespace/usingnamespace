import logging
log = logging.getLogger(__name__)

from uuid import UUID

from pyramid.compat import string_types

from .... import models as m

class Entries(object):
    """Entries

    Traversal object for a site ID
    """

    __name__ = None
    __parent__ = None

    def __init__(self):
        self.__name__ = 'entries'

        log.debug("Entries!")

    def __getitem__(self, key):
        """Check to see if we can traverse this ..."""

        next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            return next_ctx

    def finalise(self, last=True):
        """Attempts to find all entries for a certain site

        :last: If this is the last context in the tree.
        :returns: None

        """
        if self.__parent__ is not None:
            # Finalise the parent first
            self.__parent__.finalise(last=True)

            # Get the entries variable from the parent
            self.site = self.__parent__.site
            self.entries = m.DBSession.query(m.Entry).filter(m.Entry.site == self.site)
        else:
            # We need a parent ...
            raise ValueError

