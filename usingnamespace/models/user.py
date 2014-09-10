import datetime

from .meta import (
        Base,
        DBSession,
        )

from sqlalchemy import (
        Column,
        DateTime,
        ForeignKey,
        Index,
        Integer,
        PrimaryKeyConstraint,
        String,
        Table,
        Unicode,
        and_,
        )

from sqlalchemy.orm import (
        contains_eager,
        noload,
        relationship,
        )

from sqlalchemy.ext.hybrid import hybrid_property

from cryptacular.bcrypt import BCRYPTPasswordManager

class User(Base):
    __table__ = Table('users', Base.metadata,
            Column('id', Integer, primary_key=True, unique=True),
            Column('email', String(256), unique=True, index=True),
            Column('name', Unicode(256), index=True),
            Column('credentials', String(60))
            )

    _email = __table__.c.email
    _credentials = __table__.c.credentials

    @hybrid_property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        manager = BCRYPTPasswordManager()
        self._credentials = manager.encode(value, rounds=14)

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.lower().strip()

    @property
    def username(self):
        """Backwards compat..."""
        return self.email

    def check_password(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.credentials, password)

    @classmethod
    def validate_user_password(cls, email, password):
        user = DBSession.query(cls).filter(cls.email == email.lower()).first()

        if user is not None:
            if user.check_password(password):
                return user
        return None

class UserTickets(Base):
    __table__ = Table('user_tickets', Base.metadata,
            Column('ticket', String(128)),
            Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
            Column('remote_addr', String(45)),
            Column('created', DateTime, default=datetime.datetime.utcnow, nullable=False),

            PrimaryKeyConstraint('ticket', 'user_id'),
            Index('ix_ticket_userid', 'ticket', 'user_id'),
            )

    user = relationship("User", lazy="joined", backref='tickets')

    @classmethod
    def find_ticket_userid(cls, ticket, userid):
        return DBSession.query(cls).join(
                User,
                and_(
                    User.email == userid.lower(),
                    User.id == cls.user_id
                    )
                ).filter(cls.ticket == ticket).options(
                            contains_eager('user')
                        ).first()

class UserAPITickets(Base):
    __table__ = Table('user_api_tickets', Base.metadata,
            Column('ticket', String(128), primary_key=True, unique=True),
            Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
            Column('remote_addr', String(45)),
            Column('created', DateTime, default=datetime.datetime.utcnow, nullable=False),
            )

    user = relationship("User", lazy="joined", backref='api_tickets')

    @classmethod
    def find_ticket(cls, ticket):
        return DBSession.query(cls).join(
                User,
                User.id == cls.user_id
                ).filter(cls.ticket == ticket).options(
                            contains_eager('user')
                        ).first()

