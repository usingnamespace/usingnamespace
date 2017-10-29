from pyramid.view import (
        view_config,
        view_defaults,
        )

@view_defaults(context='...traversal.v1.Entries',
        route_name='api',
        renderer='json',
        )
class Site:
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
                    'title': entry.title,
                    #'entry': entry.current_revision.entry,
                    'tags': [tag.tag for tag in entry.tags],
                    'published': {
                            'year': entry.year,
                            'month': entry.month,
                            'day': entry.day,
                            'time': entry.time,
                            } if entry.pubdate else {},
                })

        return {'entries': entries}
