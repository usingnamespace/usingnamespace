import logging
log = logging.getLogger(__name__)

from pyramid.config import (
        Configurator,
        not_,
        )
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config
from sqlalchemy.exc import DBAPIError

from models import DBSession

required_settings = [
        'pyramid.secret.session',
        'pyramid.secret.auth',
        'usingnamespace.upload_path',
        'usingnamespace.management.domain',
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
    _session_factory = UnencryptedCookieSessionFactoryConfig(
            settings['pyramid.secret.session'],
            cookie_httponly=True,
            cookie_max_age=864000
            )

    # Create the authentication policy, we are using a stock one
    _authn_policy = AuthTktAuthenticationPolicy(
            settings['pyramid.secret.auth'],
            max_age=864000,
            http_only=True,
            debug=True,
            hashalg='sha512',
            callback=lambda x, y: 0,
            )

    # The stock standard authorization policy will suffice for our needs
    _authz_policy = ACLAuthorizationPolicy()

    config.set_session_factory(_session_factory)
    config.set_authentication_policy(_authn_policy)
    config.set_authorization_policy(_authz_policy)

    config.include(add_routes)
    config.include(add_views)
    config.include(add_events)

    # Set-up deform so that it uses bootstrap
    config.include('deform_bootstrap')

    # Add in pyramid_mailer for sending out emails
    config.include('pyramid_mailer')

    def cur_domain(request):
        host = request.host if ":" not in request.host else request.host.split(":")[0]

        return host

    config.set_request_property(cur_domain, 'domain', reify=True)

    return config.make_wsgi_app()

def add_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static', cache_max_age=3600)
    config.add_static_view('files', config.registry.settings['usingnamespace.upload_path'], cache_max_age=3600)

    def management(info, request):
        if config.registry.settings['usingnamespace.management.domain'] == request.domain:
            log.debug("Management is request.host: {}".format(request.domain))
            return True
        else:
            log.debug("This is not a management domain: {}".format(request.domain))
            return False

    # Used so that in the future we can set up a route for the management interface seperately
    config.add_route('main', '/*traverse', use_global_views=True, custom_predicates=(not_(management),))
    config.add_route('management', '/*traverse', use_global_views=False, custom_predicates=(management,))

def add_views(config):
    # Scan the views sub-module
    config.scan('.views')

    # Error pages
    #config.add_view('usingnamespace.views.errors.db_failed', context=DBAPIError, renderer='db_failed.mako')

    # Add a slash if the view has not been found.
    config.add_notfound_view('usingnamespace.views.errors.not_found', renderer='not_found.mako', append_slash=True)

def add_events(config):
    config.add_subscriber('usingnamespace.events.view_helpers.view_helpers',
            'pyramid.events.BeforeRender')

def route_zero_extend_month_day(request, elements, kw):
    if 'day' in kw:
        kw['day'] = "{0:02d}".format(kw['day'])
    if 'month' in kw:
        kw['month'] = "{0:02d}".format(kw['month'])

    return elements, kw
