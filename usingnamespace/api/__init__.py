from pyramid.config import Configurator
from pyramid.wsgi import wsgiapp2
from pyramid.settings import asbool

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
    application = make_application(config.registry.settings, config.registry)

    # Add the API route
    route_kw = {}

    if config.registry.settings['usingnamespace.api.domain'] != '':
        route_kw['is_api_domain'] = config.registry.settings['usingnamespace.api.domain']

    config.add_route_predicate('is_api_domain', config.maybe_dotted('.predicates.route.API'))
    config.add_route('usingnamespace.api',
            config.registry.settings['usingnamespace.api.route_path'] + '/*subpath',
            **route_kw)

    # Add the API view
    config.add_view(wsgiapp2(application), route_name='usingnamespace.api')

def make_application(settings, parent_registry):
    config = Configurator()
    config.registry.settings.update(settings)
    config.registry.parent_registry = parent_registry

    def is_api(request):
        if request.matched_route is not None and request.matched_route.name == 'usingnamespace.api.main':
            return True
        return False

    config.add_request_method(callable=is_api, name='is_api', reify=True)
    config.add_subscriber_predicate('is_api', config.maybe_dotted('.predicates.subscriber.IsAPI'))

    config.add_route('usingnamespace.api.main',
            '/*traverse',
            factory='.traversal.Root',
            use_global_views=False,
            )

    config.scan('.views')

    return config.make_wsgi_app()

def main(global_config, **settings):
    pass
