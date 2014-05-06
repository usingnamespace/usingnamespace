from pyramid.view import view_config

from sqlalchemy.orm import undefer

from ..models import (
    DBSession,
    Entry,
    )

from .finalisecontext import FinaliseContext

class Home(FinaliseContext):
    @view_config(context='..traversal.MainRoot', renderer='templates/chronological.mako')
    def main(self):
        # Get the latest 10 entries that are published

        entries = self.context.entries.filter(Entry.pubdate != None).order_by(Entry.pubdate.desc()).options(undefer('current_revision.entry')).slice(0, 10).all()

        return {
                'entries': entries
                }

