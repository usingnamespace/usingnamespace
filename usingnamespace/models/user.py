# File: User.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

from meta import (
        Base,
        DBSession,
        )

from sqlalchemy import (
        Table,
        Column,
        Integer,
        Unicode,
        String,
        )

from sqlalchemy.ext.hybrid import hybrid_property

from cryptacular.bcrypt import BCRYPTPasswordManager

class User(Base):
    __table__ = Table('users', Base.metadata,
            Column('id', Integer, primary_key=True, unique=True),
            Column('email', String(256), unique=True, index=True),
            Column('name', Unicode(256), index=True),
            Column('credentials', String(60))
            )

    _email = __table__.c.email
    _credentials = __table__.c.credentials

    @hybrid_property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        manager = BCRYPTPasswordManager()
        self._credentials = manager.encode(value, rounds=14)

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.lower().strip()

    @property
    def username(self):
        """Backwards compat..."""
        return self.email

    def check_password(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.credentials, password)

    @classmethod
    def validate_user_password(cls, email, password):
        user = DBSession.query(cls).filter(cls.email == email.lower()).first()

        if user is not None:
            if user.check_password(password):
                return user
        return None

