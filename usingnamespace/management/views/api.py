import logging
log = logging.getLogger(__name__)

from pyramid.view import (
        view_config,
        view_defaults,
        notfound_view_config,
        )
from pyramid.config import not_
from pyramid.httpexceptions import (
        HTTPForbidden,
        HTTPSeeOther,
        )
from pyramid.security import (
        unauthenticated_userid,
        authenticated_userid,
        )

from ...api.ticket import APITicket

from ..forms.api import (
        APIForm,
        )

@view_defaults(
        context='..traversal.API',
        route_name='management',
        effective_principals='system.Authenticated',
        )
class API(object):
    """Provides the views for the API ticket management"""

    def __init__(self, context, request):
        """Initialises the view class

        :context: The traversal context
        :request: The current request

        """
        self.context = context
        self.request = request

    @view_config(
            renderer='templates/api.mako',
            )
    def api(self):
        api_tickets = APITicket(self.request).find_existing(self.request.user.user.email)

        (schema, f) = APIForm.create_form(request=self.request,
                action=self.request.current_route_url())

        return {
                'form': f.render(),
                'tickets': api_tickets,
                }

    @view_config(
            renderer='templates/api.mako',
            request_method='POST',
            )
    def api_submit(self):
        controls = self.request.POST.items()
        (schema, f) = APIForm.create_form(request=self.request,
                action=self.request.current_route_url())

        try:
            appstruct = f.validate(controls)
            ticket_maker = APITicket(self.request)

            ticket_maker.new(self.request.user.user.email, self.request)

            return HTTPSeeOther(location=self.request.current_route_url())
        except ValidationFailure as e:
            if e.field['csrf_token'].error is not None:
                e.field.error = e.field['csrf_token'].error
                e.field['csrf_token'].cstruct = self.request.session.get_csrf_token()

            return {
                    'form': e.render(),
                    }
