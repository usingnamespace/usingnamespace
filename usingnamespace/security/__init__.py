# Package

# File: auth.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2013-02-08

import random
import string

from pyramid import security

from pyramid.security import (
        unauthenticated_userid,
        Authenticated,
        Everyone,
    )

from pyramid.interfaces import (
    IAuthenticationPolicy,
    )

from pyramid.authorization import ACLAuthorizationPolicy

from authentication import AuthPolicy

def user(request):
    userid = unauthenticated_userid(request)

    # Get the current authentication policy
    req = request.registry
    policy = req.queryUtility(IAuthenticationPolicy)
    if policy is None:
        return None

    # Have the authentication policy find the information for us
    ticket = policy.find_user_ticket(request)

    class UserInfo(object):
        def __init__(self):
            self.id = None
            self.auth = {}
            self.user = None
            self.ticket = None

    userinfo = UserInfo()

    if ticket is None:
        return userinfo

    userinfo.id = ticket.user.email
    userinfo.user = ticket.user
    userinfo.ticket = ticket

    return userinfo

def includeme(config):
    _authn_policy = AuthPolicy(
            config.registry.settings['pyramid.secret.auth'],
            max_age=864000,
            http_only=True,
            debug=True,
            hashalg='sha512',
            )

    # The stock standard authorization policy will suffice for our needs
    _authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(_authn_policy)
    config.set_authorization_policy(_authz_policy)

    config.add_request_method('..utils.RequestStorage', name='state', property=True, reify=True)
    config.add_request_method(user, name='user', property=True, reify=True)
