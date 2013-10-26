from pyramid.view import (
        view_config,
        view_defaults,
        )

@view_defaults(
        context='..traversal.ManagementRoot',
        route_name='management'
        )
class Management(object):
    """Provide all of the views for the main page of management"""

    def __init__(self, context, request):
        """Initialises the view class

        :context: The traversal context
        :request: The current request

        """
        self.context = context
        self.request = request

    @view_config(
            renderer='management/home.mako',
            effective_principals='system.Authenticated',
            )
    def home(self):
        return {}
