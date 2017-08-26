from sqlalchemy.orm import configure_mappers

from .entry import (
    Entry,
    Revision,
    EntryAuthors,
    EntryRevisions,
    Tag,
    RevisionTags,
)

from .user import (
    User,
    UserTickets,
    UserAPITickets,
)

from .domain import (
    Domain,
)

from .site import (
    Site,
)

# run configure mappers to ensure we avoid any race conditions
configure_mappers()
