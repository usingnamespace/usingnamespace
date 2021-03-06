# File: Post.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

import datetime

from .meta import Base

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
        Unicode,
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
        backref,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        )

from sqlalchemy.ext.mutable import Mutable, MutableComposite
from sqlalchemy.dialects.postgresql import UUID

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
        return ', '.join(map(str, (map(sql.desc, map(str, self.__clause_element__().clauses)))))

    def asc(self):
        return ', '.join(map(str, (map(sql.asc, map(str, self.__clause_element__().clauses)))))

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
            Column('id', UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True),
            Column('parent', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=True),
            Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('title', Text, nullable=False),
            Column('entry', Text, nullable=False),
            Column('rendered', Text, nullable=True),
            Column('format', String(25), default="markdown", nullable=False),
            Column('changes', Text, nullable=True),
            Column('created', DateTime, server_default=text('current_timestamp')),
            Column('modified', DateTime, server_default=None, server_onupdate=text('current_timestamp'), nullable=True),
            Column('pubdate', DateTime, nullable=True),
            )

    # Defer loading from this, we don't need it most of the time.
    entry = deferred(__table__.c.entry)

    author = relationship("User")
    tags = relationship("Tag", secondary="revision_tags")

class Entry(Base):
    __table__ = Table('entries', Base.metadata,
            Column('id', UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True),
            Column('current_rev', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('slug', Unicode(128)),
            Column('created', DateTime, server_default=text('current_timestamp'), index=True),
            Column('modified', DateTime, server_default=None, server_onupdate=text('current_timestamp'), nullable=True),
            Column('year', Integer, server_default=None, index=True, nullable=True),
            Column('month', Integer, server_default=None, index=True, nullable=True),
            Column('day', Integer, server_default=None, index=True, nullable=True),
            Column('time', Time, nullable=True),
            Column('site_id', ForeignKey('sites.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False, index=True),

            Index('idx_site_year_month_day_slug', 'site_id', 'year', 'month', 'day', 'slug', unique=True),
            Index('idx_site_year_month_day', 'site_id', 'year', 'month', 'day'),
            Index('idx_site_year_month', 'site_id', 'year', 'month'),
            Index('idx_site_year', 'site_id', 'year'),
            )

    current_revision = relationship("Revision", lazy="joined", uselist=False)
    all_revisions = relationship("Revision", secondary="entry_revisions")
    authors = relationship("User", secondary="entry_authors")
    site = relationship("Site", backref=backref("entries", lazy="dynamic"))

    _time = __table__.c.time
    _pubdate = composite(PublishedDateTime, 'year', 'month', 'day', '_time', comparator_factory=PublishedDateTimeComparator)

    @property
    def title(self):
        return self.current_revision.title

    @property
    def entry(self):
            return self.current_revision.rendered

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
        if isinstance(self, Entry):
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

class EntryRevisions(Base):
    __table__ = Table('entry_revisions', Base.metadata,
            Column('entry_id', ForeignKey('entries.id', onupdate="CASCADE", ondelete="CASCADE"), index=True, nullable=False),
            Column('revision_id', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),

            PrimaryKeyConstraint('entry_id', 'revision_id'),
            )

class EntryAuthors(Base):
    __table__ = Table('entry_authors', Base.metadata,
            Column('entry_id', ForeignKey('entries.id', onupdate="CASCADE", ondelete="CASCADE"), index=True, nullable=False),
            Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('revision_id', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
            Column('primary', Boolean, default=False),

            PrimaryKeyConstraint('entry_id', 'user_id'),
            )

class Tag(Base):
    __table__ = Table('tags', Base.metadata,
            Column('id', UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True),
            Column('tag', String(50), index=True, unique=True),
            Column('description', Text),
            )

class RevisionTags(Base):
    __table__ = Table('revision_tags', Base.metadata,
            Column('revision_id', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE")),
            Column('tag_id', ForeignKey('tags.id', onupdate="CASCADE", ondelete="CASCADE")),

            PrimaryKeyConstraint('revision_id', 'tag_id'),
            )


