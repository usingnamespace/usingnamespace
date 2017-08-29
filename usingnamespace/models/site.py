from .meta import Base

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    String,
    Table,
    text,
)

from sqlalchemy.orm import (
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

class Site(Base):
    __table__ = Table('sites', Base.metadata,
            Column('id', UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True),
            Column('title', String(256)),
            Column('tagline', String(256)),
            Column('owner_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False, index=True),
            )

    owner = relationship("User", backref="sites")
