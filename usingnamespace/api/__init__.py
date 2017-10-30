import logging

from pyramid.config import Configurator
from pyramid.wsgi import wsgiapp2
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid_authsanity.sources import HeaderAuthSourceInitializer
from pyramid_authsanity.interfaces import IAuthSourceService

log = logging.getLogger(__name__)

required_settings = [
    'usingnamespace.secret.auth',
]

default_settings = (
    ('route_path', str, '/api'),
    ('domain', str, ''),
)

# Stolen from pyramid_debugtoolbar
def parse_settings(settings):
    parsed = {}

    def populate(name, convert, default):
        name = '%s%s' % ('usingnamespace.api.', name)
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

    if config.registry.settings['usingnamespace.api.domain'] != '':
        route_kw['is_api_domain'] = config.registry.settings['usingnamespace.api.domain']

        config.add_route_predicate(
            'is_api_domain',
            config.maybe_dotted('.predicates.route.API')
        )

    config.add_route(
        'usingnamespace.api',
        config.registry.settings['usingnamespace.api.route_path'] + '/*subpath',
        **route_kw)

    # Add the API view
    config.add_view(wsgiapp2(application), route_name='usingnamespace.api')

def make_sub_application(settings, parent_registry):
    config = Configurator()
    config.registry.settings.update(settings)
    config.registry.parent_registry = parent_registry

    make_application(config)

    return config.make_wsgi_app()

def make_application(config):
    settings = config.registry.settings
    do_start = True

    for _req in required_settings:
        if _req not in settings:
            log.error('{} is not set in configuration file.'.format(_req))
            do_start = False

    if do_start is False:
        log.error('Unable to start due to missing configuration')
        exit(-1)

    config.include('pyramid_retry')
    config.include('pyramid_services')
    config.include('pyramid_mailer')
    config.include('pyramid_authsanity')

    # Register the Authorization Header Source
    config.register_service_factory(
        HeaderAuthSourceInitializer(
            settings['usingnamespace.secret.auth'],
        ),
        iface=IAuthSourceService
    )
    config.set_authorization_policy(ACLAuthorizationPolicy())

    config.include('..models.meta')

    def is_api(request):
        if (
            request.matched_route is not None and
            request.matched_route.name == 'usingnamespace.api.main'
        ):
            return True
        return False

    config.add_request_method(callable=is_api, name='is_api', reify=True)
    config.add_subscriber_predicate(
        'is_api',
        config.maybe_dotted('.predicates.subscriber.IsAPI')
    )

    config.add_route(
        'api',
        '/*traverse',
        factory='.traversal.Root',
        use_global_views=False,
    )

    config.scan('.views')

def main(global_config, **app_settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings = global_config.copy()
    settings.update(app_settings)

    do_start = True

    for _req in required_settings:
        if _req not in settings:
            log.error('{} is not set in configuration file.'.format(_req))
            do_start = False

    if do_start is False:
        log.error('Unable to start due to missing configuration')
        exit(-1)

    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
    config = Configurator(settings=settings)

    # Go parse the settings
    settings = parse_settings(config.registry.settings)

    # Update the config
    config.registry.settings.update(settings)

    make_application(config)

    return config.make_wsgi_app()
