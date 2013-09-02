# File: Post.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

import datetime

from meta import Base

from sqlalchemy import (
        Boolean,
        Column,
        DateTime,
        ForeignKey,
        ForeignKeyConstraint,
        Index,
        Integer,
        PrimaryKeyConstraint,
        Sequence,
        String,
        Table,
        Text,
        Time,
        UniqueConstraint,
        extract,
        sql,
        text,
        )

from sqlalchemy.orm.properties import CompositeProperty

from sqlalchemy.orm import (
        composite,
        deferred,
        relationship,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        )

from sqlalchemy.ext.mutable import Mutable, MutableComposite

class PublishedDateTimeComparator(CompositeProperty.Comparator):
    def __eq__(self, other):
        """redefine the equals operator"""

        if not isinstance(other, PublishedDateTime):
            raise ValueError

        if isinstance(other, datetime.datetime):
            other = PublishedDateTime(other.year, other.month, other.day, other.timetz())

        return sql.and_(*[a == b for a, b in
                          zip(self.__clause_element__().clauses,
                              other.__composite_values__())])
    def __ne__(self, other):
        """redefine the not equals operator"""

        if other is None:
            return sql.and_(*[a != None for a in self.__clause_element__().clauses])

        return sql.and_(*[a != b for a, b in
                        zip(self.__clause_element__().clauses,
                            other.__composite_values__())])

    def desc(self):
        return sql.desc(', '.join(map(str, self.__clause_element__().clauses)))

    def asc(self):
        return sql.asc(', '.join(map(str, self.__clause_element__().clauses)))

class PublishedDateTime(MutableComposite):
    def __init__(self, year, month, day, time):
        if year is not None and month is not None and day is not None:
            try:
                valid = datetime.date(year, month, day)
            except:
                raise

            self.year = year
            self.month = month
            self.day = day
            self.time = time
        else:
            self.year = self.month = self.day = None

    def getdatetime(self):
        return datetime.datetime.combine(datetime.date(self.year, self.month, self.day), self.time)

    def __setattr__(self, key, value):
        # Set the attributes
        super(MutableComposite, self).__setattr__(key, value)

        # Alert all parents to the change
        self.changed()

    def __composite_values__(self):
        return self.year, self.month, self.day, self.time

    def __repr__(self):
        return u'<PublishedDateTime: year: %d month: %d day: %d time: %d>' % (self.year, self.month, self.day, self.time.strftime("%H:%M") if self.strftime is not None else None)

    def __eq__(self, other):
        return isinstance(other, PublishedDateTime) and \
                other.year == self.year and \
                other.month == self.month and \
                other.day == self.day and \
                other.time == self.time

    def __ne__(self, other):
        return not self.__eq__(other)

class Revision(Base):
    __table__ = Table('revisions', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('parent', Integer, ForeignKey('revisions.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=True),
            Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('title', Text, nullable=False),
            Column('entry', Text, nullable=False),
            Column('format', String(25), default="markdown", nullable=False),
            Column('changes', Text, nullable=True),
            Column('created', DateTime, server_default=text('current_timestamp')),
            Column('modified', DateTime, server_default=None, server_onupdate=text('current_timestamp'), nullable=True),
            Column('pubdate', DateTime, nullable=True),
            )

    # Defer loading from this, we don't need it most of the time.
    entry = deferred(__table__.c.entry)

    author = relationship("User")
    entry_rendered = relationship("RevisionRendered")
    tags = relationship("Tag", secondary="revision_tags")

class Entry(Base):
    __table__ = Table('entries', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('current_rev', Integer, ForeignKey('revisions.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('slug', String(128), index=True),
            Column('created', DateTime, server_default=text('current_timestamp'), index=True),
            Column('modified', DateTime, server_default=None, server_onupdate=text('current_timestamp'), nullable=True),
            Column('year', Integer(4), server_default=None, index=True, nullable=True),
            Column('month', Integer(2), server_default=None, index=True, nullable=True),
            Column('day', Integer(2), server_default=None, index=True, nullable=True),
            Column('time', Time, nullable=True),
            Column('domain_id', Integer, ForeignKey('domains.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),

            UniqueConstraint('year', 'month', 'day', 'slug'),
            Index('idx_year_month_day', 'year', 'month', 'day'),
            Index('idx_year_month', 'year', 'month'),
            )

    current_revision = relationship("Revision", lazy="joined")
    all_revisions = relationship("Revision", secondary="entry_revisions")
    authors = relationship("User", secondary="entry_authors")

    _time = __table__.c.time
    _pubdate = composite(PublishedDateTime, 'year', 'month', 'day', '_time', comparator_factory=PublishedDateTimeComparator)

    @property
    def title(self):
        return self.current_revision.title

    @property
    def entry(self):
        return self.current_revision.entry_rendered

    @property
    def tags(self):
            return self.current_revision.tags

    @property
    def time(self):
        if self.pubdate is not None:
            return self.pubdate.strftime("%H:%M")
        else:
            return None

    @hybrid_property
    def pubdate(self):
        # Depending on the time, we may be some internal SQLAlchemy instance,
        # or we may be our good ol' self PublishedDateTime. If we are the
        # latter, we return a datetime object which is what most people are
        # expecting anyway.
        if isinstance(self._pubdate, PublishedDateTime):
            return self._pubdate.getdatetime()
        return self._pubdate

    @pubdate.setter
    def pubdate_set(self, value):
        if not isinstance(value, PublishedDateTime):
            if isinstance(value, datetime.datetime):
                self._pubdate = PublishedDateTime(value.year, value.month, value.day, value.timetz())
            else:
                raise ValueError
        else:
            self._pubdate = value

class RevisionRendered(Base):
    __table__ = Table('revision_rendered', Base.metadata,
            Column('revision_id', Integer, ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
            Column('entry', Text, nullable=False),
            )

class EntryRevisions(Base):
    __table__ = Table('entry_revisions', Base.metadata,
            Column('entry_id', Integer, ForeignKey('entries.id', onupdate="CASCADE", ondelete="CASCADE"), index=True, nullable=False),
            Column('revision_id', Integer, ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),

            PrimaryKeyConstraint('entry_id', 'revision_id'),
            )

class EntryAuthors(Base):
    __table__ = Table('entry_authors', Base.metadata,
            Column('entry_id', Integer, ForeignKey('entries.id', onupdate="CASCADE", ondelete="CASCADE"), index=True, nullable=False),
            Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('revision_id', Integer, ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
            Column('primary', Boolean, default=False),

            PrimaryKeyConstraint('entry_id', 'user_id'),
            )

class Tag(Base):
    __table__ = Table('tags', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('tag', String(50), index=True, unique=True),
            Column('description', Text),
            )

class RevisionTags(Base):
    __table__ = Table('revision_tags', Base.metadata,
            Column('revision_id', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE")),
            Column('tag_id', ForeignKey('tags.id', onupdate="CASCADE", ondelete="CASCADE")),

            PrimaryKeyConstraint('revision_id', 'tag_id'),
            )


