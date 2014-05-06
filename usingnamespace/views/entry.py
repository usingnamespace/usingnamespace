from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.orm import undefer

from ..models import (
    DBSession,
    Entry,
    )

from .finalisecontext import FinaliseContext

class Entry(FinaliseContext):

    @view_config(context='..traversal.Entry', renderer='templates/permapage.mako')
    def single(self):
        return {
                'post': self.context.entry,
                }

