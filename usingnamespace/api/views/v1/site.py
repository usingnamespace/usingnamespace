from pyramid.view import (
        view_config,
        view_defaults,
        )

from ....views.finalisecontext import FinaliseContext

@view_defaults(context='...traversal.v1.Site',
        route_name='api',
        renderer='json',
        )
class Site(FinaliseContext):
    @view_config()
    def main(self):
        entries = []

        for entry in self.context.entries.all():
            entries.append({
                    'id': entry.id,
                    'title': entry.title,
                    'year': entry.year,
                    'month': entry.month,
                    'day': entry.day,
                    'time': entry.time,
                })

        return {
                'entries': entries,
                }


