from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently

from sqlalchemy.orm import undefer

from ..models import (
    DBSession,
    Entry,
    Revision,
    Tag,
    RevisionTags,
    )

def home(request):
    # Get the latest 10 entries that are published
    entries = DBSession.query(Entry).filter(Entry.pubdate != None).order_by(Entry.pubdate.desc()).options(undefer('current_revision.entry')).slice(0, 10).all()

    return {'entries': entries}

def redirhome(request):
    url = request.route_url('uns.home')
    return HTTPMovedPermanently(location=url)

