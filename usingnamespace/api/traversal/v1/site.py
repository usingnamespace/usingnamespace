import logging
log = logging.getLogger(__name__)

from uuid import UUID

from pyramid.compat import string_types

from .... import models as m

class Site(object):
    """Site

    Traversal object for a site ID
    """

    __name__ = None
    __parent__ = None

    def __init__(self, site_id):
        """Create the default root object

        :request: The Pyramid request object
        """
        log.debug("Creating new Site: {}".format(site_id))
    
        try:
            self.id = UUID(site_id)
        except ValueError:
            raise ValueError('Invalid site ID')
        
        self.__name__ = '{}'.format(self.id)

    def __getitem__(self, key):
        """Check to see if we can traverse this ..."""

        next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            return next_ctx

    def finalise(self, last=True):
        """Attempts to find out if the site ID is valid

        :last: If this is the last context in the tree.
        :returns: None

        """
        if self.__parent__ is not None:
            # Finalise the parent first
            self.__parent__.finalise(last=False)

            # Get the entries variable from the parent
            self.site = self.__parent__.sites
            self.site = self.site.filter(m.Site.id == self.id)
        else:
            # We need a parent ...
            raise ValueError

        if last:
            # Attempt to get a single entry, if we get nothing back we return
            # ValueError
            first = self.site.first()

            if first is None:
                raise ValueError('Site ID ({}) is not valid for current user ({})'.format(self.id, self.__parent__._request.user.user.email))

            else:
                self.site = first

