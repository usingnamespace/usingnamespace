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
    pass

def route_zero_extend_month_day(request, elements, kw):
    if 'day' in kw:
        kw['day'] = "{0:02d}".format(kw['day'])
    if 'month' in kw:
        kw['month'] = "{0:02d}".format(kw['month'])

    return elements, kw
