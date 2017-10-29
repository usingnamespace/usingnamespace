import logging

from pyramid.config import Configurator
from pyramid.settings import asbool

log = logging.getLogger(__name__)

required_settings = [
    'usingnamespace.name',
    'usingnamespace.api.sub',
]

def includeme(config):
    config.include('pyramid_retry')
    config.include('pyramid_services')
    config.include('pyramid_mako')
    config.include('pyramid_mailer')

    config.include('.models.meta')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(
        'files',
        config.registry.settings['usingnamespace.upload_path'],
        cache_max_age=3600
    )

    config.add_route(
        'main',
        '/*traverse',
        use_global_views=True
    )

    config.scan('.views')
    config.scan('.subscribers')


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
    config = Configurator(settings=settings, root_factory='.traversal.MainRoot')
    config.include('.')

    if asbool(settings['usingnamespace.api.sub']) is True:
        config.include('.api')

    return config.make_wsgi_app()
