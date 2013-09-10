from pyramid.view import view_config


class Management(object):
    """Authentication provides views for things related to authentication"""

    def __init__(self, context, request):
        """Initialises the view class

        :context: The traversal context
        :request: The current request

        """
        self.context = context
        self.request = request
    
    @view_config(
            context='..traversal.ManagementRoot',
            route_name='management',
            renderer='management/home.mako',
            )
    def home(self):
        return {}
