import logging
log = logging.getLogger(__name__)

from pyramid.view import (
        view_config,
        view_defaults,
        forbidden_view_config,
        )

from pyramid.security import (
        remember,
        forget,
        )
from pyramid.httpexceptions import (
        HTTPForbidden,
        HTTPSeeOther,
        )

from deform import ValidationFailure

from ..forms.user import (
        LoginForm,
        )

@view_defaults(context='..traversal.ManagementRoot', route_name='management')
class Authentication(object):
    """Authentication provides views for things related to authentication"""

    def __init__(self, context, request):
        """Initialises the view class

        :context: The traversal context
        :request: The current request

        """
        self.context = context
        self.request = request

    @view_config(
            name='auth',
            renderer='management/authenticate.mako',
            )
    def authenticate(self):
        if self.request.authenticated_userid is not None:
            return HTTPSeeOther(location=self.request.route_url('management',
                traverse=self.request.session.get('next', '')))

        (schema, f) = LoginForm.create_form(request=self.request,
                action=self.request.current_route_url())
        return {
                'form': f.render(),
                }

    @view_config(
            name='auth',
            renderer='management/authenticate.mako',
            request_method='POST',
            )
    def authenticate_submit(self):
        controls = self.request.POST.items()
        (schema, f) = LoginForm.create_form(request=self.request,
                action=self.request.current_route_url())
        try:
            appstruct = f.validate(controls)
            headers = remember(self.request, appstruct['email'])

            log.debug("Sending user to: {}".format(self.request.session.get('next', None)))
            return HTTPSeeOther(location=self.request.route_url(
                'management', traverse=self.request.session.get('next', '')),
                headers = headers)
        except ValidationFailure as e:
            if e.field['csrf_token'].error is not None:
                e.field.error = e.field['csrf_token'].error
                e.field['csrf_token'].cstruct = self.request.session.get_csrf_token()

            return {
                    'form': e.render(),
                    }

    @view_config(
            name='deauth',
            )
    def deauth(self):
        headers = forget(self.request)

        return HTTPSeeOther(location=self.request.route_url('management',
            traverse=''), headers = headers)

    @view_config(
            context=HTTPForbidden,
            containment='..traversal.ManagementRoot',
            renderer='string',
            )
    def forbidden(self):
        # Check to see if a user is already logged in...
        if self.request.authenticated_userid:
            request.response.status_int = 403
            return {}

        if self.request.path != '/':
            self.request.session['next'] = self.request.path
        return HTTPSeeOther(location=self.request.route_url(
            'management', traverse='auth'))
