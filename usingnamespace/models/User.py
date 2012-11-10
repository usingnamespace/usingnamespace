# File: User.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

from meta import Base

from sqlalchemy import (
        Table,
        Column,
        Integer,
        String
        )

class User(Base):
    __table__ = Table('users', Base.metadata,
            Column('id', Integer, primary_key=True, unique=True),
            Column('username', String(128), unique=True, index=True),
            Column('realname', String(256), index=True),
            Column('credentials', String(40))
            )

