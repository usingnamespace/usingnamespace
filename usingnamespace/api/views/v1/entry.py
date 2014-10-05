from pyramid.view import (
        view_config,
        view_defaults,
        )

from ....views.finalisecontext import FinaliseContext

@view_defaults(context='...traversal.v1.Entry',
        route_name='api',
        renderer='json',
        )
class Site(FinaliseContext):
    @view_config()
    def main(self):
        entry = self.context.entry

        return {
                'id': str(entry.id),
                'slug': entry.slug,
                #'created': entry.created, # Convert to string
                #'modified': entry.modified, # Convert to string
                'title': entry.title,
                'entry': entry.current_revision.entry,
                'tags': [tag.tag for tag in entry.tags],
                'published': {
                        'year': entry.year,
                        'month': entry.month,
                        'day': entry.day,
                        'time': entry.time,
                        } if entry.pubdate else {},
              }
