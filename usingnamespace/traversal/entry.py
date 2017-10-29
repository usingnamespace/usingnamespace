import logging

from .. import models as m

log = logging.getLogger(__name__)

class Entry(object):
    """The leaf node for an entry"""

    __parent__ = None
    entries = None

    def __init__(self, slug):
        """Initialises the Entry context.

        :name: The slug for this particular entry

        """
        log.debug("Creating new Entry: {}".format(slug))
        self.__name__ = slug

    @property
    def entries(self):
        if self.__parent__ is not None:
            # Get the entries variable from the parent
            entries = self.__parent__.entries
            return entries.filter(m.Entry.slug == self.__name__)
        else:
            # We need a parent ...
            raise ValueError

    @property
    def entry(self):
        self.entry = self.entries.first()

        if self.entry is None:
            raise ValueError
