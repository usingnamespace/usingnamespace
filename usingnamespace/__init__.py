import logging
log = logging.getLogger(__name__)

from pyramid.config import (
        Configurator,
        not_,
        )
from pyramid.session import SignedCookieSessionFactory

from sqlalchemy import engine_from_config
from sqlalchemy.exc import DBAPIError

from .models import DBSession

from .security.authentication import AuthPolicy

required_settings = [
        'pyramid.secret.session',
        'pyramid.secret.auth',
        'usingnamespace.upload_path',
        'usingnamespace.management.domain',
        'usingnamespace.name',
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings, root_factory='.traversal.MainRoot')

    do_start = True

    for _req in required_settings:
        if _req not in settings:
            log.error('{} is not set in configuration file.'.format(_req))
            do_start = False

    if do_start is False:
        log.error('Unable to start due to missing configuration')
        exit(-1)

    # Create the session factory, we are using the stock one
    _session_factory = SignedCookieSessionFactory(
            settings['pyramid.secret.session'],
            httponly=True,
            max_age=864000
            )

    config.set_session_factory(_session_factory)

    # Include our security stuff
    config.include('.security')

    # We use mako for template rendering
    config.include('pyramid_mako')

    # Set-up pyramid_deform
    config.include('pyramid_deform')

    # Add in pyramid_mailer for sending out emails
    config.include('pyramid_mailer')

    def is_management(request):
        if request.matched_route is not None and request.matched_route.name == 'management':
            return True
        return False

    config.add_request_method(callable=is_management, name='is_management', reify=True)
    config.add_route_predicate('is_management_domain', config.maybe_dotted('.predicates.route.Management'))
    config.add_subscriber_predicate('is_management', config.maybe_dotted('.predicates.subscriber.IsManagement'))

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static', cache_max_age=3600)
    config.add_static_view('files', config.registry.settings['usingnamespace.upload_path'], cache_max_age=3600)

    # Used so that in the future we can set up a route for the management interface seperately
    config.add_route('management',
            '/*traverse',
            use_global_views=False,
            factory='.traversal.ManagementRoot',
            is_management_domain=config.registry.settings['usingnamespace.management.domain']
            )

    config.add_route('main',
            '/*traverse',
            use_global_views=True
            )

    # Scan the views sub-module
    config.scan('.views')

    # Scan the subscribers for events sub-module
    config.scan('.subscribers')

    return config.make_wsgi_app()
