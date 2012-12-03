from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.session import UnencryptedCookieSessionFactoryConfig

from models import DBSession

from sqlalchemy.exc import DBAPIError

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.set_session_factory(UnencryptedCookieSessionFactoryConfig(settings['pyramid.secretcookie']))
    config.include(add_routes)
    config.include(add_views)
    config.include(add_events)
    return config.make_wsgi_app()

def add_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('uns.home', '/')

    # Set up the routes for "archive" urls. year/month/day
    config.add_route('uns.year.month.day.title', '/{year:\d{4}}/{month:\d{2}}/{day:\d{2}}/{title}/')
    config.add_route('uns.year.month.day', '/{year:\d{4}}/{month:\d{2}}/{day:\d{2}}/')
    config.add_route('uns.year.month', '/{year:\d{4}}/{month:\d{2}}/')
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
    config.add_view('usingnamespace.views.home', route_name='uns.home',
            renderer='chronological.mako')
    config.add_view('usingnamespace.views.home', route_name='uns.home.pagenonum', renderer='site.mako')

    # Error pages
    #config.add_view('usingnamespace.views.errors.db_failed', context=DBAPIError, renderer='db_failed.mako')

def add_events(config):
    pass
