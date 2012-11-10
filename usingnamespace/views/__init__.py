from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Entry,
    Revision,
    )

def home(request):
    # Get the latest 10 entries that are published
    posts = DBSession.query(Entry).filter(Entry.pubdate != None).order_by(Entry.pubdate.desc()).slice(0, 10).all()

    return {'posts': posts}


