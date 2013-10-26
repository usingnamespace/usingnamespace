# File: Domain.py
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

class Domain(Base):
    __table__ = Table('domains', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('domain', String(256), index=True, unique=True),
            Column('site_id', Integer, ForeignKey('sites.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            )

    site = relationship("Site", lazy="joined")

