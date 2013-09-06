from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.orm import undefer

from ..models import (
    DBSession,
    Entry,
    )

from FinaliseContext import FinaliseContext

class Entry(FinaliseContext):

    @view_config(context='..traversal.SingleEntry', renderer='permapage.mako')
    def single(self):
        return {
                'post': self.context.entry,
                }

