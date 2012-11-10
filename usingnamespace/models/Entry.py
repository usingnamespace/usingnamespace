# File: Post.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

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
        UniqueConstraint,
        text,
        )

from sqlalchemy.orm import (
        relationship,
        deferred,
        )

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

class Entry(Base):
    __table__ = Table('entries', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('current_rev', Integer, ForeignKey('revisions.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
            Column('slug', String(128), index=True),
            Column('created', DateTime, server_default=text('current_timestamp'), index=True),
            Column('modified', DateTime, server_default=None, server_onupdate=text('current_timestamp'), nullable=True),
            Column('pubdate', DateTime, nullable=True, index=True),

            UniqueConstraint('pubdate', 'slug'),
            )

    current_revision = relationship("Revision", lazy="joined")
    all_revisions = relationship("Revision", secondary="entry_revisions")
    authors = relationship("User", secondary="entry_authors")

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
