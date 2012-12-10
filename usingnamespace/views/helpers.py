from pyramid.url import route_url

from ..models import Entry

class URLHelper(object):
    """Helps generate URL's in Templates

    This is a simple class that given either an Entry or year/month/day (or
    parts thereof) will generate a valid URL
    """

    def __init__(self, current_request):
        super(URLHelper, self).__init__()
        self.request = current_request

    def y_archive(self, *args, **kw):
        if len(args) == 0:
            raise ValueError

        if isinstance(args[0], Entry):
            kw['year'] = args[0].year
        else:
            kw['year'] = args[0]

        return route_url('uns.year', self.request, **kw)

    def ym_archive(self, *args, **kw):
        if len(args) == 0:
            raise ValueError

        if isinstance(args[0], Entry):
            kw['year'] = args[0].year
            kw['month'] = args[0].month
        else:
            if len(args) < 2:
                raise ValueError

            kw['year'] = args[0]
            kw['month'] = args[1]

        return route_url('uns.year.month', self.request, **kw)

    def ymd_archive(self, *args, **kw):
        if len(args) == 0:
            raise ValueError

        if isinstance(args[0], Entry):
            kw['year'] = args[0].year
            kw['month'] = args[0].month
            kw['day'] = args[0].day
        else:
            if len(args) < 3:
                raise ValueError

            kw['year'] = args[0]
            kw['month'] = args[1]
            kw['day'] = args[2]

        return route_url('uns.year.month.day', self.request, **kw)

    def entry(self, *args, **kw):
        if len(args) == 0:
            raise ValueError

        if isinstance(args[0], Entry):
            kw['year'] = args[0].year
            kw['month'] = args[0].month
            kw['day'] = args[0].day
            kw['title'] = args[0].slug
        else:
            if len(args) < 4:
                raise ValueError

            kw['year'] = args[0]
            kw['month'] = args[1]
            kw['day'] = args[2]
            kw['title'] = args[3]

        return route_url('uns.year.month.day.title', self.request, **kw)

