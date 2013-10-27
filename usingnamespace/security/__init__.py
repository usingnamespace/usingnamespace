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

def _clean_principal(princid):
    """ Utility function that cleans up the passed in principal

    This can easily also be extended for example to make sure that certain
    usernames are automatically off-limits.
    """
    if princid in (Authenticated, Everyone):
        princid = None
    return princid

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

