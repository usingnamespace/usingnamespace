# File: Site.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2013-09-02

from pyramid.compat import (
        text_type,
        binary_type
        )

from .meta import Base

from sqlalchemy import (
        Boolean,
        Column,
        ForeignKey,
        Integer,
        PrimaryKeyConstraint,
        String,
        Table,
        Unicode,
        text,
        )

from sqlalchemy.orm import (
        relationship,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        Comparator,
        )

from sqlalchemy.dialects.postgresql import UUID

class Site(Base):
    __table__ = Table('sites', Base.metadata,
            Column('id', UUID, server_default=text("uuid_generate_v4()"), primary_key=True, index=True),
            Column('title', String(256)),
            Column('tagline', String(256)),
            Column('owner_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False, index=True),
            )

    owner = relationship("User", backref="sites")

