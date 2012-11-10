import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

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
    with transaction.manager:
        user = User()
        user.username = "xistence"
        user.realname = "Bert JW Regeer"
        user.credentials = "test"

        DBSession.add(user)
        DBSession.flush()

        user = user.id

    insert_new_rev_entry("one", "Post number 1", "one", user)
    insert_new_rev_entry("two", "Post number 2", "two", user)
    insert_new_rev_entry("three", "Post number 3", "three", user)
    insert_new_rev_entry("four", "Post number 4", "four", user)
    insert_new_rev_entry("five", "Post number 5", "five", user)

def insert_new_rev_entry(title, entry, slug, user, published=False):
    with transaction.manager:
        revision = Revision()
        revision.revision = 0
        revision.user_id = user
        revision.title = title
        revision.entry = entry

        DBSession.add(revision) 
        DBSession.flush()

        entry = Entry()
        entry.user_id = user
        entry.rev_id = revision.id
        entry.rev_num = revision.revision
        entry.slug = slug
        if published:
            entry.pubdate = datetime.now()

        DBSession.add(entry)
        DBSession.flush()
