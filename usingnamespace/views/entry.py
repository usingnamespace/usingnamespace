from pyramid.view import view_config

    )

from .finalisecontext import FinaliseContext

class Entry(FinaliseContext):

    @view_config(context='..traversal.Entry', renderer='templates/permapage.mako')
    def single(self):
        return {
                'post': self.context.entry,
                }

