import random
import string

from pyramid import security

from models import (
        DBSession,
        User,
        )

def remember(request, principal, **kw):
    """
    Remember the user, and create a new session ticket

    First we create a brand new ticket, add it for the user to the database as
    a valid ticket, then we call security.remember() which does the actual work
    of creating the cookie that is going to get sent to the user.
    """

    ticket = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(128))

    if 'tokens' in kw:
        kw['tokens'].append('tkt_' + ticket)
    else:
        kw['tokens'] = ['tkt_' + ticket]

    return security.remember(request, principal, **kw)

def forget(request):
    """
    Forget the users session/ticket

    This removes the users session/ticket entirely, unsets the cookie as well
    as removing the ticket from the database.
    """
    
    return security.forget(request)
