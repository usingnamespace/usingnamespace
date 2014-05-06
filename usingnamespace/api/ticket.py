import logging
log = logging.getLogger(__name__)

import random
import string
import base64

from sqlalchemy.orm import joinedload

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

from ..models import (
        DBSession,
        User,
        UserAPITickets,
        )

from .interfaces import ISerializer

class APITicket(object):
    def __init__(self, request):
        self.request = request

    def find_existing(self, principal):
        request = self.request
        user = DBSession.query(User).filter(User.email == principal).options(joinedload('api_tickets')).first()

        serializer = self.request.registry.queryUtility(ISerializer, 'apiticket')

        api_tickets = []
        for ticket in user.api_tickets:
            t = serializer.dumps({
                'principal': principal,
                'auth_ticket': ticket.ticket,
                })
            t = base64.b64encode(t)
            t = t.decode('utf-8')

            # Split the result up into multiple strings, that are 32 bytes long each.
            t = [t[i:i+64] for i in range(0, len(t), 64)]

            api_tickets.append(t)

        return api_tickets

    def new(self, principal, tokens = None):
        request = self.request
        value = {}
        value['principal'] = principal
        value['auth_ticket'] = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(64))
        value['tokens'] = tokens if tokens is not None else []

        user = DBSession.query(User).filter(User.email == principal).first()

        if user is None:
            raise ValueError('Invalid principal provided')

        ticket = value['auth_ticket']
        remote_addr = request.environ['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.environ else None
        user.api_tickets.append(UserAPITickets(ticket=ticket, remote_addr=remote_addr))

    def forget(self):
        request = self.request
        debug = self.debug
        user = request.user

        if user.ticket:
            debug and self._log('forgetting user: %s, removing ticket: %s' % (user.id, user.ticket.ticket), 'forget', request)
            DBSession.delete(user.ticket)


def includeme(config):
    serializer = SignedSerializer(
            config.registry.settings['pyramid.secret.auth'],
            salt='usingnamespace.api.ticket',
            hashalg='sha512',
            )

    config.registry.registerUtility(serializer, ISerializer, 'apiticket')
