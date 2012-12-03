from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.orm import undefer
from sqlalchemy.sql import extract

from ..models import (
    DBSession,
    Entry,
    Revision,
    Tag,
    RevisionTags,
    )

def _year_month_day_query(year, month, day):
    return _year_month_query(year, month).filter(Entry.day == day)

def _year_month_query(year, month):
    return _year_query(year).filter(Entry.month == month)

def _year_query(year):
    return DBSession.query(Entry).filter(Entry.year == year)

def article(request):
    print(request)
    return {}
    pass

def ymd_list(request):
    entries = _year_month_day_query(request.matchdict['year'], request.matchdict['month'], request.matchdict['day']).order_by(Entry.pubdate.desc()).all()

    return {'entries': entries}

def ym_list(request):
    entries = _year_month_query(request.matchdict['year'], request.matchdict['month']).order_by(Entry.pubdate.desc()).all()

    return {'entries': entries}

def y_list(request):
    entries = _year_query(request.matchdict['year']).order_by(Entry.pubdate.desc()).all()

    return {'entries': entries,
            'year': request.matchdict['year']
            }
