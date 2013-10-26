import logging
log = logging.getLogger(__name__)

from ..models import (
            Entry,
        )

class SingleEntry(object):
    """The leaf node for an entry"""

    __parent__ = None
    entries = None

    def __init__(self, slug):
        """Initialises the Entry context.

        :name: The slug for this particular entry

        """
        log.debug("Creating new Entry: {}".format(slug))
        self.__name__ = slug

    def finalise(self, last=True):
        """Attempts to find out if the slug is valid!

        :last: If this is the last context in the tree
        :returns: None

        """
        if self.__parent__ is not None:
            # Finalise the parent first
            self.__parent__.finalise(last=False)

            # Get the entries variable from the parent
            self.entries = self.__parent__.entries
            self.entries = self.entries.filter(Entry.slug == self.__name__)
        else:
            # We need a parent ...
            raise ValueError

        if last:
            # Attempt to get the entry, if we get nothing back we return
            # ValueError
            self.entry = self.entries.first()

            if self.entry is None:
                raise ValueError
