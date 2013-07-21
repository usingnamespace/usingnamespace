import unittest
import transaction

from pyramid import testing

from ..models import *

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.config import Configurator
from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import os

ROOT_PATH = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(ROOT_PATH, '..', '..', 'config', 'test.ini')
setup_logging(CONFIG_PATH)
from meta import settings

def setup():
    engine = engine_from_config(settings, prefix='sqlalchemy.')

    config = Configurator(settings=settings)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

def teardown():
    engine = engine_from_config(settings, prefix='sqlalchemy.')

    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)


