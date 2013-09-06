from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.orm import undefer

from ..models import (
    DBSession,
    Entry,
    )








