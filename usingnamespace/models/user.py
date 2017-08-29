import datetime

from .meta import (
    Base,
)

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    String,
    Table,
    Unicode,
    text,
)

from sqlalchemy.orm import (
    relationship,
)

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __table__ = Table(
        'users', Base.metadata,
        Column('id', UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True, unique=True),
        Column('email', String(256), unique=True, index=True),
        Column('name', Unicode(256), index=True),
        Column('credentials', String(60)),
        Column('disabled', Boolean()),
        Column('deleted', Boolean()),
    )

    _email = __table__.c.email

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.lower().strip()


class UserTickets(Base):
    __table__ = Table(
        'user_tickets', Base.metadata,
        Column('ticket', String(128)),
        Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
        Column('remote_addr', String(45)),
        Column('created', DateTime, default=datetime.datetime.utcnow, nullable=False),

        PrimaryKeyConstraint('ticket', 'user_id'),
        Index('ix_ticket_userid', 'ticket', 'user_id'),
    )

    user = relationship("User", lazy="joined", backref='tickets')


class UserAPITickets(Base):
    __table__ = Table(
        'user_api_tickets', Base.metadata,
        Column('ticket', String(128), primary_key=True, unique=True),
        Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
        Column('remote_addr', String(45)),
        Column('created', DateTime, default=datetime.datetime.utcnow, nullable=False),
    )

    user = relationship("User", lazy="joined", backref='api_tickets')
