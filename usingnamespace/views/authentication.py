from pyramid.view import view_config

import deform
from deform import Form

from ..forms.user import (
        LoginForm,
        )

class Authentication(object):
    """Authentication provides views for things related to authentication"""

    def __init__(self, context, request):
        """Initialises the view class

        :context: The traversal context
        :request: The current request

        """
        self.context = context
        self.request = request

    @view_config(context='..traversal.ManagementRoot',
            name='auth',
            route_name='management',
            renderer='management/authenticate.mako',
            )
    def authenticate(self):
        schema = LoginForm().bind(request=self.request)
        f = Form(schema, action=self.request.current_route_url(),
                buttons=(deform.form.Button(name='Submit', css_class='btn btn-primary'),), css_class='testing')
        return {
                'form': f.render(),
                }

    @view_config(context='..traversal.ManagementRoot',
            name='auth',
            route_name='management',
            request_method='POST'
            )
    def authenticate_submit(self):
        return {}

    @view_config(context='..traversal.ManagementRoot',
            name='deauth',
            route_name='management',
            )
    def deauth(self):
        return {}
