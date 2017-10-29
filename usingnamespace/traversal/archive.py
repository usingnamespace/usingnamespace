import logging

from zope.interface import Interface
from zope.interface import implementer

from pyramid.compat import string_types

from .entry import Entry

from .. import models as m

log = logging.getLogger(__name__)

class IArchive(Interface):
    """Marker interface for archive contexts"""


@implementer(IArchive)
class ArchiveYear(object):
    """ArchiveYear is the context for this years archives"""

    __parent__ = None
    entries = None

    def __init__(self, year):
        """Initialises the context

        :year: The year we are trying to get archives for

        """
        log.debug("Creating new ArchiveYear: {}".format(year))

        if isinstance(year, int):
            self.__name__ = '{}'.format(year)
            self.year = year

        if isinstance(year, string_types):
            self.__name__ = year

            try:
                self.year = int(year)
            except ValueError:
                raise ValueError('Year is not valid.')

    def __getitem__(self, key):
        """Return the next item in the traversal tree

        :key: The next item to look for
        :returns: The next traversal item

        """
        next_ctx = None

        if key == 'page':
            pass

        # Last resort, see if it is a valid month
        try:
            next_ctx = ArchiveYearMonth(key)
        except ValueError:
            next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            next_ctx._request = self._request
            return next_ctx

    @property
    def entries(self):
        if self.__parent__ is not None:
            # Get the entries variable from the parent
            entries = self.__parent__.entries
            return entries.filter(m.Entry.year == self.year)
        else:
            raise ValueError


@implementer(IArchive)
class ArchiveYearMonth(object):
    """ArchiveYearMonth is the context for the year/month archives"""

    __parent__ = None
    entries = None

    def __init__(self, month):
        """Initialises the context

        :month: The month we are getting archives for

        """
        log.debug("Creating new ArchiveYearMonth: {}".format(month))

        if isinstance(month, int):
            self.__name__ = '{}'.format(month)
            self.month = month

        if isinstance(month, string_types):
            self.__name__ = month

            try:
                self.month = int(month)

                if self.month > 12 or self.month < 1:
                    raise ValueError
            except ValueError:
                raise ValueError('Month is not valid.')

    def __getitem__(self, key):
        """Return the next item in the traversal tree

        :key: The next item to look for
        :returns: The next traversal item

        """
        next_ctx = None

        if key == 'page':
            pass

        # Last resort, see if it is a valid day
        try:
            next_ctx = ArchiveYearMonthDay(key)
        except ValueError:
            next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            next_ctx._request = self._request
            return next_ctx

    @property
    def entries(self):
        if self.__parent__ is not None:
            # Get the entries variable from the parent
            entries = self.__parent__.entries
            return entries.filter(m.Entry.month == self.month)
        else:
            raise ValueError


@implementer(IArchive)
class ArchiveYearMonthDay(object):
    """ArchiveYearMonthDay is the context for the year/month/day archives"""

    __parent__ = None
    entries = None

    def __init__(self, day):
        """Initialises the context

        :day: The day we are getting archives for

        """
        log.debug("Creating new ArchiveYearMonthDay: {}".format(day))

        if isinstance(day, int):
            self.__name__ = '{}'.format(day)
            self.day = day

        if isinstance(day, string_types):
            self.__name__ = day

            try:
                self.day = int(day)

                if self.day > 31 or self.day < 1:
                    raise ValueError
            except ValueError:
                raise ValueError('Day is not valid.')

    def __getitem__(self, key):
        """Return the next item in the traversal tree

        :key: The next item to look for
        :returns: The next traversal item

        """
        next_ctx = None

        if key == 'page':
            pass

        # Last resort, see if it is a valid slug
        try:
            next_ctx = Entry(key)
        except ValueError:
            next_ctx = None

        if next_ctx is None:
            raise KeyError
        else:
            next_ctx.__parent__ = self
            next_ctx._request = self._request
            return next_ctx

    @property
    def entries(self):
        if self.__parent__ is not None:
            # Get the entries variable from the parent
            entries = self.__parent__.entries
            return entries.filter(m.Entry.day == self.day)
        else:
            raise ValueError
