# File: Post.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

import datetime

from meta import Base

from sqlalchemy import (
        Boolean,
        Column,
        DateTime,
        Date,
        Time,
        ForeignKey,
        ForeignKeyConstraint,
        Index,
        Integer,
        PrimaryKeyConstraint,
        Sequence,
        String,
        Table,
        Text,
        UniqueConstraint,
        text,
        )

from sqlalchemy.orm import (
        relationship,
        deferred,
        composite,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        )

from sqlalchemy.ext.mutable import Mutable, MutableComposite

class _date(object):
    def __get__(self, obj, type=None):
        if obj is None:
            return None
        if obj.year is None:
            return None
        else:
            datetime.date(obj.year, obj.month, obj.day)

    def __set__(self, obj, value):
        if value is None:
            obj.year = obj.month = obj.day = None
            return

        obj.year = value.year
        obj.month = value.month
        obj.day = value.day

class Date(MutableComposite):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, Date):
            if isinstance(value, datetime.datetime):
                return Date(value.year, value.month, value.day)

            return MutableComposite.coerce(key, value)
        else:
            return value

    datetime  = _date()
    def __init__(self, year, month, day):
        if year is not None and month is not None and day is not None:
            try:
                valid = datetime.date(year, month, day)
            except:
                raise

            self.year = year
            self.month = month
            self.day = day
        else:
            self.year = self.month = self.day = None

    def __setattr__(self, key, value):
        # Set the attributes
        super(MutableComposite, self).__setattr__(key, value)

        # Alert all parents to the change
        self.changed()

    def __composite_values__(self):
        return self.year, self.month, self.day

    def __repr__(self):
        return u'<Date: year: %d month: %d day: %d>' % (self.year, self.month, self.day)

    def __eq__(self, other):
        return isinstance(other, Date) and \
                other.year == self.year and \
                other.month == self.month and \
                other.day == self.day

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
            Column('pubtime', Time, index=True, nullable=True),

            UniqueConstraint('year', 'month', 'day', 'slug'),
            )

    current_revision = relationship("Revision", lazy="joined")
    all_revisions = relationship("Revision", secondary="entry_revisions")
    authors = relationship("User", secondary="entry_authors")

    pubdate = composite(Date, 'year', 'month', 'day')

    _pubtime = __table__.c.pubtime

    @property
    def title(self):
        return self.current_revision.title

    @property
    def tags(self):
            return self.current_revision.tags

    @property
    def time(self):
        if self.pubtime is not None:
            return self.pubtime.strftime('%H:%M')
        else:
            return None

    @hybrid_property
    def pubtime(self):
        return self._pubtime

    @pubtime.setter
    def pubtime(self, value):
        if isinstance(value, datetime.datetime):
            self._pubtime = value
        else:
            raise ValueError

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
            Column('tag', String(50), index=True),
            Column('description', Text),
            )

class RevisionTags(Base):
    __table__ = Table('revision_tags', Base.metadata,
            Column('revision_id', ForeignKey('revisions.id', onupdate="CASCADE", ondelete="CASCADE")),
            Column('tag_id', ForeignKey('tags.id', onupdate="CASCADE", ondelete="CASCADE")),

            PrimaryKeyConstraint('revision_id', 'tag_id'),
            )


