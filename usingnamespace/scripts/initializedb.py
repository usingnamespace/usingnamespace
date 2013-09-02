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

defaults = {
            'users': [
                (u'xistence', 'Bert JW Regeer', 'test')
                ],
            'tags': [
                (u'c++', "The C++ programming language"),
                (u'c', "The C progrmaming langauge"),
                (u'database', "Databases store stuff"),
                (u'testing', "Not sure..."),
                (u'not used', "Don't look at me that way"),
                ],
            'domains': [
                (u'test.alexandra.network.lan', "xistence"),
                (u'whatever.alexandra.network.lan', "xistence"),
                ],
            'entries': [
                # Title, entry, slug, user, tags, published
                (u'one', u'Post number 1', 'one', 1, ["c++", "c"], u'test.alexandra.network.lan', True),
                (u'two', u'Post number 2', 'two', 1, ["database", "testing"], u'test.alexandra.network.lan', True),
                (u'three', u'Post number 3', 'three', 1, ["c++", "database"], u'whatever.alexandra.network.lan', True),
                (u'four', u'Post number 4', 'four', 1, ["testing", "c"], u'whatever.alexandra.network.lan', True),
                (u'five', u'Post number 5', 'five', 1, ["c++", "c", "database"], u'test.alexandra.network.lan', True),
                (u'No tags', u'This post has no tags', 'no-tags', 1, [], u'whatever.alexandra.network.lan', True),
                ],
        }

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
        for (u, r, c) in defaults['users']:
            sp = transaction.savepoint()
            try:
                user = User(username=u, realname=r, credentials=c)
                DBSession.add(user)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print 'Username "{}" already exists.'.format(u)

        for (t, d) in defaults['tags']:
            sp = transaction.savepoint()
            try:
                tag = Tag(tag = t, description = d)
                DBSession.add(tag)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print 'Tag "{}" already exists.'.format(t)

        for (d, o) in defaults['domains']:
            sp = transaction.savepoint()
            try:
                domain = Domain(domain = d, owner = DBSession.query(User).filter(User.username == o).first().id)
                DBSession.add(domain)
                DBSession.flush()
            except IntegrityError:
                print e
                sp.rollback()
                print 'Domain "{}" already exists.'.format(d)

        for (t, e, s, u, ta, d, p) in defaults['entries']:
            sp = transaction.savepoint()
            try:
                insert_new_rev_entry(t, e, s, u, ta, d, published=p)
            except IntegrityError:
                sp.rollback()
                print 'Entry "{}" already exists.'.format(t)


def insert_new_rev_entry(title, entry, slug, user, tags, domain, published=False):
    revision = Revision()
    revision.revision = 0
    revision.user_id = user
    revision.title = title
    revision.entry = entry

    for tag in tags:
        revision.tags.append(DBSession.query(Tag).filter(Tag.tag == tag).first())

    DBSession.add(revision)
    DBSession.flush()

    entry = Entry(current_rev = revision.id, slug = slug, domain_id = DBSession.query(Domain).filter(Domain.domain == domain).first().id)
    if published:
        entry.pubdate = datetime.datetime.now()

    DBSession.add(entry)
    DBSession.flush()

    author = EntryAuthors()
    author.entry_id = entry.id
    author.user_id = user
    author.revision_id = revision.id

    DBSession.add(entry)
    DBSession.flush()
