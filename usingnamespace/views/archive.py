from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.orm import undefer

from ..models import (
    DBSession,
    Entry,
    )

from FinaliseContext import FinaliseContext

class Archive(FinaliseContext):

    @view_config(context='..traversal.ArchiveYear', renderer='yearly.mako')
    def year(self):
        entries = self.context.entries.order_by(Entry.pubdate.desc()).options(undefer('current_revision.entry')).all()

        return {
                'entries': entries,
                'year': self.context.year,
                }

    @view_config(context='..traversal.ArchiveYearMonth', renderer='chronological.mako')
    def month(self):
        entries = self.context.entries.order_by(Entry.pubdate.desc()).options(undefer('current_revision.entry')).all()

        return {
                'entries': entries,
                }

    @view_config(context='..traversal.ArchiveYearMonthDay',
            renderer='chronological.mako')
    def day(self):
        entries = self.context.entries.order_by(Entry.pubdate.desc()).options(undefer('current_revision.entry')).all()

        return {
                'entries': entries,
                }
