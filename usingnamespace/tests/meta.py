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
settings = get_appsettings(CONFIG_PATH)
setup_logging(CONFIG_PATH)

class DBBaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        DBSession.configure(bind=cls.engine)

    def setUp(self):
        self.connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = DBSession(bind=self.connection)
        Base.session = self.session

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()
        self.session.close()
        self.connection.close()
        DBSession.remove()
