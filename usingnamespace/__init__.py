import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator

from sqlalchemy import engine_from_config
from sqlalchemy.exc import DBAPIError

from .models import DBSession

required_settings = [
        'usingnamespace.name',
        ]

def main(global_config, **app_settings):
    """ This function returns a Pyramid WSGI application.
    """

    settings = global_config.copy()
    settings.update(app_settings)

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

    # Include the transaction manager
    config.include('pyramid_tm')

    # We use mako for template rendering
    config.include('pyramid_mako')

    # Set-up pyramid_deform
    config.include('pyramid_deform')

    # Add in pyramid_mailer for sending out emails
    config.include('pyramid_mailer')

    # Add in the API...
    config.include('.api')

    # Add in the Management interface...
    config.include('.management')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static', cache_max_age=3600)
    config.add_static_view('files', config.registry.settings['usingnamespace.upload_path'], cache_max_age=3600)

    config.add_route('main',
            '/*traverse',
            use_global_views=True
            )

    # Scan the views sub-module
    config.scan('.views')

    # Scan the subscribers for events sub-module
    config.scan('.subscribers')

    return config.make_wsgi_app()
