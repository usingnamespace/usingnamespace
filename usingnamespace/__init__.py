import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
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
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)

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

    return config.make_wsgi_app()

def add_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static', cache_max_age=3600)
    config.add_static_view('files', config.registry.settings['usingnamespace.upload_path'], cache_max_age=3600)

    config.add_route('uns.home', '/')

    # Set up the routes for "archive" urls. year/month/day
    config.add_route('uns.year.month.day.title', '/{year:\d{4}}/{month:\d{2}}/{day:\d{2}}/{title}/', pregenerator=route_zero_extend_month_day)
    config.add_route('uns.year.month.day', '/{year:\d{4}}/{month:\d{2}}/{day:\d{2}}/', pregenerator=route_zero_extend_month_day)
    config.add_route('uns.year.month', '/{year:\d{4}}/{month:\d{2}}/', pregenerator=route_zero_extend_month_day)
    config.add_route('uns.year', '/{year:\d{4}}/')

    # Set up routes for tags
    config.add_route('uns.tag', '/tag/{tagname}/')
    config.add_route('uns.tagnoname', '/tag/')
    config.add_route('uns.tags', '/tags/')

    # Backwards compatible routes. Blogofile created these. May end up keeping them.
    config.add_route('uns.home.pagenonum', '/page/')
    config.add_route('uns.home.page', '/page/{num:\d+}/')

    # Management routes
    config.add_route('uns.management', '/manage/')
    config.add_route('uns.management.posts', '/manage/posts/')

def add_views(config):
    config.add_view('usingnamespace.views.home.home', route_name='uns.home',
            renderer='chronological.mako')
    config.add_view('usingnamespace.views.home.redirhome',
            route_name='uns.home.pagenonum')

    config.add_view('usingnamespace.views.archive.article', route_name='uns.year.month.day.title', renderer='permapage.mako')
    config.add_view('usingnamespace.views.archive.ymd_list', route_name='uns.year.month.day', renderer='chronological.mako')
    config.add_view('usingnamespace.views.archive.ym_list', route_name='uns.year.month', renderer='chronological.mako')
    config.add_view('usingnamespace.views.archive.y_list', route_name='uns.year', renderer='yearly.mako')

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
