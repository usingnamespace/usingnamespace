import logging
log = logging.getLogger(__name__)

import random
import string

from zope.interface import implementer

from webob.cookies import SignedSerializer

from pyramid.interfaces import (
    IAuthenticationPolicy,
    IDebugLogger,
    )

from pyramid.security import (
    Authenticated,
    Everyone,
    )

from ...models import (
        DBSession,
        User,
        UserAPITickets,
        )

from ..interfaces import ISerializer

def _clean_principal(princid):
    """ Utility function that cleans up the passed in principal

    This can easily also be extended for example to make sure that certain
    usernames are automatically off-limits.
    """
    if princid in (Authenticated, Everyone):
        princid = None
    return princid

def _get_auth_header(request):
    serializer = request.registry.queryUtility(ISerializer, 'apiticket')

    try:
        return serializer.loads(request.headers['x-api-ticket'])
    except:
        return None

@implementer(IAuthenticationPolicy)
class AuthPolicy(object):
    def _log(self, msg, methodname, request):
        logger = request.registry.queryUtility(IDebugLogger)
        if logger:
            cls = self.__class__
            classname = cls.__module__ + '.' + cls.__name__
            methodname = classname + '.' + methodname
            logger.debug(methodname + ': ' + msg)

    def __init__(self,
                 secret,
                 debug=False,
                 hashalg='sha512',
                 ):
        self.debug = debug

    def unauthenticated_userid(self, request):
        """ The userid key within the auth_tkt cookie."""

        result = _get_auth_header(request)

        self.debug and self._log('Got result from x-api-ticket: %s' % (result,), 'unauthenticated_userid', request)

        if result:
            principal = result['principal']
            if _clean_principal(principal) is None:
                self.debug and self._log('use of principal %r is disallowed by any '
                        'built-in Pyramid security policy, returning None' %
                        principal)
                return None

            auth = {'principal': principal}

            if 'tokens' in result:
                auth['tokens'] = result['tokens']

            if 'auth_ticket' in result:
                auth['ticket'] = result['auth_ticket']

            request.state['auth'] = auth

            return principal

    def authenticated_userid(self, request):
        """ Return the authenticated userid or ``None``."""
        userid = request.user.id

        return userid

    def find_user_ticket(self, request):
        """ Return the user object if valid for the ticket or ``None``."""

        auth = request.state.get('auth', {})
        ticket = auth.get('ticket', '')
        principal = auth.get('principal', '')

        if not ticket or not principal:
            return None

        ticket = UserAPITickets.find_ticket_userid(ticket, principal)

        if ticket is None:
            self.debug and self._log('No ticket found', 'find_user_ticket', request)
            self.cookie.set_cookies(request.response, '', max_age=0)

        return ticket

    def effective_principals(self, request):
        """ A list of effective principals derived from request.

        This will return a list of principals including, at least,
        :data:`pyramid.security.Everyone`. If there is no authenticated
        userid, or the ``callback`` returns ``None``, this will be the
        only principal:

        .. code-block:: python

            return [Everyone]

        """
        debug = self.debug
        effective_principals = [Everyone]
        userid = self.authenticated_userid(request)

        if userid is None:
            debug and self._log(
                'authenticated_userid returned %r; returning %r' % (
                    userid, effective_principals),
                'effective_principals',
                request
                )
            return effective_principals

        groups = []

        # Get the groups here ...

        effective_principals.append(Authenticated)
        effective_principals.append(userid)
        effective_principals.extend(groups)

        debug and self._log(
            'returning effective principals: %r' % (
                effective_principals,),
            'effective_principals',
            request
             )
        return effective_principals


    def remember(self, request, principal, tokens=None, **kw):
        raise NotImplemented("This should never be called ...")

    def forget(self, request):
        raise NotImplemented("This should never be called ...")

