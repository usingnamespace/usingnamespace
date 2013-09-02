# File: Domain.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2013-09-02

from meta import Base

from sqlalchemy import (
        Boolean,
        Column,
        ForeignKey,
        Table,
        Integer,
        Unicode,
        PrimaryKeyConstraint,
        UniqueConstraint,
        )

class Domain(Base):
    __table__ = Table('domains', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('domain', Unicode(256), index=True, unique=True),
            Column('owner', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            )

