import random
import string

from pyramid import security

from pyramid.security import (
        Authenticated,
        Everyone,
    )

from pyramid.interfaces import (
    IAuthenticationPolicy,
    )

from pyramid.authorization import ACLAuthorizationPolicy

from .authentication import AuthPolicy

def user(request):
    userid = request.authenticated_userid
    
    return request.state['auth']['userinfo']

def includeme(config):
    _authn_policy = AuthPolicy(
            config.registry.settings['pyramid.secret.auth'],
            debug=True,
            hashalg='sha512',
            )

    # The stock standard authorization policy will suffice for our needs
    _authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(_authn_policy)
    config.set_authorization_policy(_authz_policy)

    config.add_request_method('..utils.RequestStorage', name='state', property=True, reify=True)
    config.add_request_method(user, name='user', property=True, reify=True)
