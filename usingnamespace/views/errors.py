from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

def db_failed(request):
    request.response.status_int = 503
    return {}

def not_found(request):
    request.response.status_int = 404
    return {}

