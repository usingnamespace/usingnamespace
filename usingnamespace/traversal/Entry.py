import logging
log = logging.getLogger(__name__)

class Entry(object):
    """The leaf node for an entry"""

    def __init__(self, slug):
        """Initialises the Entry context.

        :name: The slug for this particular entry

        """
        log.debug("Creating new Entry: {}".format(slug))
        self.__name__ = slug
