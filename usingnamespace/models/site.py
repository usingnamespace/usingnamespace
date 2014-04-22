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
            other = other.encode("idna")
        elif isinstance(other, binary_type):
            other = other
        else:
            raise ValueError("Unable to encode to IDNA format.")

        return self.__clause_element__() == other

class Site(Base):
    __table__ = Table('sites', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('idna', String(128), unique=True, index=True),
            Column('title', String(256)),
            Column('tagline', String(256)),
            Column('owner_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            )

    _idna = __table__.c.idna

    @hybrid_property
    def idna(self):
        if isinstance(self, Site):
            return self._idna.encode('ascii').decode("idna")
        return self._idna

    @idna.setter
    def idna(self, value):
        if isinstance(value, text_type):
            self._idna = value.encode("idna")
        elif isinstance(value, binary_type):
            self._idna = value
        else:
            raise ValueError("Unable to store value as requested.")

    @idna.comparator
    def idna(cls):
        return IdnaComparator(cls._idna)

    owner = relationship("User", backref="sites")

