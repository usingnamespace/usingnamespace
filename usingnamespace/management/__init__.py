import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.wsgi import wsgiapp2

required_settings = [
        'pyramid.secret.session',
        'pyramid.secret.auth',
        'usingnamespace.upload_path',
        'sqlalchemy.url',
        ]

default_settings = (
    ('route_path', str, '/management'),
    ('domain', str, ''),
)

# Stolen from pyramid_debugtoolbar
def parse_settings(settings):
    parsed = {}

    def populate(name, convert, default):
        name = '%s%s' % ('usingnamespace.management.', name)
        value = convert(settings.get(name, default))
        parsed[name] = value
    for name, convert, default in default_settings:
        populate(name, convert, default)
    return parsed

def includeme(config):
    # Go parse the settings
    settings = parse_settings(config.registry.settings)

    # Update the config
    config.registry.settings.update(settings)

    # Create the application
    application = make_sub_application(config.registry.settings, config.registry)

    # Add the API route
    route_kw = {}

    if config.registry.settings['usingnamespace.management.domain'] != '':
        route_kw['is_management_domain'] = config.registry.settings['usingnamespace.management.domain']

    config.add_route_predicate('is_management_domain', config.maybe_dotted('.predicates.route.Management'))
    config.add_route('usingnamespace.management',
            config.registry.settings['usingnamespace.management.route_path'] + '/*subpath', 
            **route_kw)

    # Add the management view
    config.add_view(wsgiapp2(application), route_name='usingnamespace.management')

def make_sub_application(settings, parent_registry):
    config = Configurator()
    config.registry.settings.update(settings)

    config.registry.parent_registry = parent_registry

    make_application(config)

    return config.make_wsgi_app()

def make_application(config):
    settings = config.registry.settings
    # Include the transaction manager
    config.include('pyramid_tm')

    # Include pyramid_mako
    config.include('pyramid_mako')

    # Include pyramid_deform
    config.include('pyramid_deform')

    # Include pyramid_mailer
    config.include('pyramid_mailer')

    # Create the session factory, we are using the stock one
    _session_factory = SignedCookieSessionFactory(
            settings['pyramid.secret.session'],
            httponly=True,
            max_age=864000
            )

    config.set_session_factory(_session_factory)

    config.include('.security')

    config.add_static_view('static', 'usingnamespace:static/', cache_max_age=3600)

    def is_management(request):
        if request.matched_route is not None and request.matched_route.name == 'usingnamespace.management.main':
            return True
        return False

    config.add_request_method(callable=is_management, name='is_management', reify=True)
    config.add_subscriber_predicate('is_management', config.maybe_dotted('.predicates.subscriber.IsManagement'))

    config.add_route('management',
            '/*traverse',
            factory='.traversal.Root',
            use_global_views=False,
            )

    config.scan('.views')
    config.scan('.subscribers')

def main(global_config, **app_settings):
    from sqlalchemy import engine_from_config
    from sqlalchemy.exc import DBAPIError

    from ..models import DBSession

    settings = global_config.copy()
    settings.update(app_settings)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)

    # Go parse the settings
    settings = parse_settings(config.registry.settings)

    # Update the config
    config.registry.settings.update(settings)

    make_application(config)

    return config.make_wsgi_app()
