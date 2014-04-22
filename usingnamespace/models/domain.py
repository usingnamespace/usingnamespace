# File: Domain.py
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
        UniqueConstraint,
        )

from sqlalchemy.orm import (
        relationship,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        Comparator,
        )

class IdnaComparator(Comparator):
    def __eq__(self, other):
        if isinstance(other, text_type):
            other = other.encode('idna').decode('utf-8')
        elif isinstance(other, binary_type):
            other = other
        else:
            raise ValueError("Unable to encode to IDNA format.")

        return self.__clause_element__() == other

class Domain(Base):
    __table__ = Table('domains', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('domain', String(256), index=True, unique=True),
            Column('site_id', Integer, ForeignKey('sites.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            )

    _domain = __table__.c.domain

    @hybrid_property
    def domain(self):
        if isinstance(self, Domain):
            return self._domain.encode('ascii').decode('idna')
        return self._domain

    @domain.setter
    def domain(self, value):
        if isinstance(value, text_type):
            self._domain = value.encode('idna').decode('utf-8')
        elif isinstance(value, binary_type):
            self._domain = value
        else:
            raise ValueError("Unable to store value as requested.")

    @domain.comparator
    def domain(cls):
        return IdnaComparator(cls._domain)

    site = relationship("Site", backref="domains", lazy="joined")

