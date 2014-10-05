import logging
log = logging.getLogger(__name__)

from uuid import UUID

from pyramid.compat import string_types
from sqlalchemy.orm import undefer

from .... import models as m

class Entry(object):
    """Entry

    Traversal object for a site ID
    """

    __name__ = None
    __parent__ = None

    def __init__(self, entry_id):
        try:
            self.id = UUID(entry_id)
        except ValueError:
            raise ValueError('Invalid entry ID')
        
        self.__name__ = '{}'.format(self.id)
        log.debug("Entry!")

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
            self.__parent__.finalise(last=False)

            # Get the entries variable from the parent
            self.entries = self.__parent__.entries
            self.entry = self.entries.filter(m.Entry.id == self.id)
        else:
            # We need a parent ...
            raise ValueError

        if last:
            self.entry = self.entry.options(undefer('current_revision.entry'))
            self.entry = self.entry.first()

            if self.entry is None:
                raise ValueError("Invalid entry ID")


