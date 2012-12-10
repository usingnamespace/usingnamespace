import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config
from sqlalchemy.exc import IntegrityError

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import *

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    try:
        with transaction.manager:
            user = User()
            user.username = "xistence"
            user.realname = "Bert JW Regeer"
            user.credentials = "test"

            DBSession.add(user)
            DBSession.flush()

            user = user.id

            tag1 = insert_new_tag("c++")
            tag2 = insert_new_tag("c")
            tag3 = insert_new_tag("database")
            tag4 = insert_new_tag("testing")
            tag5 = insert_new_tag("not used")

            insert_new_rev_entry("one", "Post number 1", "one", user, [tag1, tag2], published=True)
            insert_new_rev_entry("two", "Post number 2", "two", user, [tag2, tag3], published=True)
            insert_new_rev_entry("three", "Post number 3", "three", user, [tag4], published=False)
            insert_new_rev_entry("four", "Post number 4", "four", user, [tag1], published=True)
            insert_new_rev_entry("five", "Post number 5", "five", user, [], published=True)
    except IntegrityError:
        pass


def insert_new_rev_entry(title, entry, slug, user, tags, published=False):
    revision = Revision()
    revision.revision = 0
    revision.user_id = user
    revision.title = title
    revision.entry = entry

    DBSession.add(revision)
    DBSession.flush()

    entry = Entry()
    entry.current_rev = revision.id
    entry.slug = slug
    if published:
        entry.pubdate = datetime.datetime.now()

    DBSession.add(entry)
    DBSession.flush()

    author = EntryAuthors()
    author.entry_id = entry.id
    author.user_id = user
    author.revision_id = revision.id

    DBSession.add(entry)

    for tag in tags:
        tagforrev = RevisionTags()

        tagforrev.revision_id = revision.id
        tagforrev.tag_id = tag
        DBSession.add(tagforrev)

    DBSession.flush()

def insert_new_tag(tagname):
    tag = Tag()
    tag.tag = tagname
    tag.description = "Unknown"

    DBSession.add(tag)
    DBSession.flush()

    return tag.id
