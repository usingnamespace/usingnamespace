from pyramid.view import view_config

from sqlalchemy.orm import undefer

from ..models import (
    Entry,
    )

class Home:
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config(context='..traversal.MainRoot', renderer='templates/chronological.mako')
    def main(self):
        # Get the latest 10 entries that are published
        entries = (
            self.context.entries.
            filter(Entry.pubdate is not None).
            order_by(Entry.pubdate.desc()).
            options(undefer('current_revision.entry')).
            slice(0, 10).
            all()
        )

        return {
            'entries': entries
        }
