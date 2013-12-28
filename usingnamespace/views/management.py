from pyramid.view import (
        view_config,
        view_defaults,
        notfound_view_config,
        )
from pyramid.config import not_
from pyramid.httpexceptions import HTTPForbidden

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

        userinfo = self.request.user

        return {
                'sites': userinfo.user.sites,
                }

@view_defaults(
        containment='..traversal.ManagementRoot',
        route_name='management'
        )
class ManagementNotAuthorized(object):
    """Anything related to management that is not authorized"""
    def __init__(self, context, request):
        """Initialises the view class

        :context: The traversal context
        :request: The current request

        """
        self.context = context
        self.request = request

    @view_config(
            effective_principals=not_('system.Authenticated')
            )
    def management_not_authed(self):
        raise HTTPForbidden()

    @notfound_view_config(
            containment='..traversal.ManagementRoot',
            renderer='string',
            )
    def management_not_found(self):
        self.request.response.status_int = 404
        return {}
