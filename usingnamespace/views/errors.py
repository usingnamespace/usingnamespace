import logging
log = logging.getLogger(__name__)

from pyramid.view import (
            view_config,
            notfound_view_config,
        )

from sqlalchemy.exc import DBAPIError

@view_config(context=DBAPIError, renderer='db_failed.mako')
def db_failed(context, request):
    log.exception(context)
    request.response.status_int = 503
    return {}

# Add a slash if the view has not been found.
@notfound_view_config(renderer='not_found.mako', append_slash=True)
def not_found(context, request):
    if request.registry.settings.get('pyramid.debug_notfound', False):
        log.exception(context)
    request.response.status_int = 404
    return {}

