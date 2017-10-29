from pyramid.view import view_config

class EntryView:
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config(
        context='..traversal.Entry',
        renderer='templates/permapage.mako'
    )
    def single(self):
        return {
            'post': self.context.entry,
        }
