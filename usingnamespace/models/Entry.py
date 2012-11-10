# File: Post.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2012-09-25

from meta import Base

from sqlalchemy import (
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
        )

class Revision(Base):
    __tablename__ = 'revisions'
    __table__ = Table('revisions', Base.metadata,
            Column('id', Integer),
            Column('revision', Integer),
            Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT")),
            Column('title', Text, nullable=False),
            Column('entry', Text, nullable=False),
            Column('changes', Text, nullable=True),
            Column('created', DateTime, server_default=text('current_timestamp')),
            Column('modified', DateTime, server_onupdate=text('current_timestamp'), nullable=True),
            Column('pubdate', DateTime, nullable=True),

            PrimaryKeyConstraint('id', 'revision'),
            UniqueConstraint('id', 'revision'),
            Index('ix_id_rev', 'id', 'revision', unique=True),
            )

class Entry(Base):
    __tablename__ = 'entries'
    __table__ = Table('entries', Base.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT")),
            Column('rev_id', Integer),
            Column('rev_num', Integer),
            Column('slug', String(128), index=True),
            Column('created', DateTime, server_default=text('current_timestamp'), index=True),
            Column('modified', DateTime, server_onupdate=text('current_timestamp')),
            Column('pubdate', DateTime, nullable=True, index=True),

            ForeignKeyConstraint(['rev_id', 'rev_num'], ['revisions.id', 'revisions.revision'], onupdate="CASCADE", ondelete="RESTRICT", name='fk_element_revision_id'),
            UniqueConstraint('pubdate', 'slug'),
            )

    currevision = relationship(Revision, lazy="joined")


