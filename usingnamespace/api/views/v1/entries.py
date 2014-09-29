from pyramid.view import (
        view_config,
        view_defaults,
        )

from ....views.finalisecontext import FinaliseContext

@view_defaults(context='...traversal.v1.Entries',
        route_name='api',
        renderer='json',
        )
class Site(FinaliseContext):
    @view_config()
    def main(self):
        db_entries = self.context.entries

        entries = []

        for entry in db_entries:
            entries.append({
                    'id': str(entry.id),
                    'slug': entry.slug,
                    #'created': entry.created, # Convert to string
                    #'modified': entry.modified, # Convert to string
                    'year': entry.year,
                    'month': entry.month,
                    'day': entry.day,
                    'time': entry.time,
                    'title': entry.title,
                    'entry': entry.current_revision.entry,
                    'tags': [tag.tag for tag in entry.tags],
                    'published': True if entry.pubdate else False,
                })

        return {'entries': entries}
