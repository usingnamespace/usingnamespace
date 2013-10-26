# File: Site.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2013-09-02

from meta import Base

from sqlalchemy import (
        Boolean,
        Column,
        ForeignKey,
        Integer,
        PrimaryKeyConstraint,
        String,
        Table,
        Unicode,
        UniqueConstraint,
        )

from sqlalchemy.orm import (
        relationship,
        )

class Site(Base):
    __table__ = Table('sites', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('title', String(256)),
            Column('tagline', String(256)),
            Column('owner_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            )

    owner = relationship("User")

