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

class User(Base):
    __table__ = Table('users', Base.metadata,
            Column('id', Integer, primary_key=True, unique=True),
            Column('email', String(256), unique=True, index=True),
            Column('name', Unicode(256), index=True),
            Column('credentials', String(60))
            )

