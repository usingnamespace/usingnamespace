import logging
log = logging.getLogger(__name__)

import random
import string

from zope.interface import implementer

from pyramid.interfaces import (
    IAuthenticationPolicy,
    IDebugLogger,
    )

from pyramid.security import (
    Authenticated,
    Everyone,
    )

from ..utils.cookies import CookieHelper

from ..security import _clean_principal

from ..models import (
        DBSession,
        User,
        UserTickets,
        )

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
                 cookie_name='auth',
                 secure=False,
                 timeout=None,
                 reissue_time=None,
                 max_age=None,
                 path="/",
                 http_only=False,
                 wild_domain=False,
                 debug=False,
                 hashalg="sha512",
                 parent_domain=False,
                 domain=None,
                 ):
        self.cookie = CookieHelper(
            secret,
            'usingnamespace-auth',
            cookie_name,
            secure=secure,
            max_age=max_age,
            http_only=http_only,
            path=path,
            wild_domain=wild_domain,
            parent_domain=parent_domain,
            domain=domain,
            hashalg=hashalg,
            )
        self.debug = debug

    def unauthenticated_userid(self, request):
        """ The userid key within the auth_tkt cookie."""
        result = self.cookie.get_cookie(request)

        if result:
            principal = result['principal']
            if _clean_principal(principal) is None:
                debug and self._log('use of principal %r is disallowed by any '
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
        """ Return the authenticated userid or ``None``.

        """
        userid = request.user.id

        return userid

    def find_user_ticket(self, request):
        """ Return the user object if valid for the ticket or ``None``. """

        auth = request.state.get('auth', {})
        ticket = auth.get('ticket', '')
        principal = auth.get('principal', '')

        if not ticket or not principal:
            return None

        ticket = UserTickets.find_ticket_userid(ticket, principal)

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


    def remember(self, request, principal, tokens=None, max_age=None):
        """ Accepts the following kw args: ``max_age=<int-seconds>``

        Return a list of headers which will set appropriate cookies on
        the response.

        """

        value = {}
        value['principal'] = principal
        value['auth_ticket'] = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(128))
        value['tokens'] = tokens if tokens is not None else []

        user = DBSession.query(User).filter(User.email == principal).first()

        if user is None:
            raise ValueError('Invalid principal provided')

        ticket = value['auth_ticket']
        remote_addr = request.environ['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.environ else None
        user.tickets.append(UserTickets(ticket=ticket, remote_addr=remote_addr))

        return self.cookie.raw_headers(request, value)

    def forget(self, request):
        """ A list of headers which will delete appropriate cookies."""

        debug = self.debug
        user = request.user

        if user.ticket:
            debug and self._log(
                    'forgetting user: %s, removing ticket: %s' % (user.id,
                        user.ticket.ticket), 'forget', request)
            DBSession.delete(user.ticket)

        return self.cookie.raw_headers(request, '', max_age=0)

