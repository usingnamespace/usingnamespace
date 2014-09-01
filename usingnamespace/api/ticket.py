import logging
log = logging.getLogger(__name__)

import random
import string
import hmac
import hashlib

from os import urandom

from pyramid.compat import bytes_

from sqlalchemy.orm import joinedload

from zope.interface import implementer

from ..models import (
        DBSession,
        User,
        UserAPITickets,
        )

from .interfaces import IDigestMethod

class APITicket(object):
    def __init__(self, request):
        self.request = request

    def find_existing(self, principal):
        request = self.request
        user = DBSession.query(User).filter(User.email == principal).options(joinedload('api_tickets')).first()

        api_tickets = []
        for ticket in user.api_tickets:
            api_tickets.append(ticket.ticket)

        return api_tickets

    def new(self, principal):
        request = self.request
        hexdigest = request.registry.queryUtility(IDigestMethod, 'apiticket')

        if hexdigest is None:
            raise ValueError('Unable to fetch digest method')

        # Get 32 bytes of random data, and sha512 it
        ticket = hexdigest(urandom(32)).hexdigest()
        user = DBSession.query(User).filter(User.email == principal).first()

        if user is None:
            raise ValueError('Invalid principal provided')

        remote_addr = request.environ['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.environ else None
        user.api_tickets.append(UserAPITickets(ticket=ticket, remote_addr=remote_addr))

def includeme(config):
    hashalg = 'sha256'
    digestmethod = lambda string=b'': hashlib.new(hashalg, string)

    config.registry.registerUtility(digestmethod, IDigestMethod, 'apiticket')
