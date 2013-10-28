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
                (u'xistence@0x58.com', u'Bert JW Regeer', 'test')
                ],
            'tags': [
                (u'c++', "The C++ programming language"),
                (u'c', "The C progrmaming langauge"),
                (u'database', "Databases store stuff"),
                (u'testing', "Not sure..."),
                (u'not used', "Don't look at me that way"),
                ],
            'sites': [
                (u'whatever', u'whatever', u'Everything and anything', "xistence@0x58.com"),
                (u'test', u'test', u'A simple test', "xistence@0x58.com"),
                (u'howdy', u'howdy', u'Another very simple test', "xistence@0x58.com"),
                (u'Ni Hao', u'\u4f60\u597d', u'A blog detailing my ventures in China', "xistence@0x58.com"),
                ],
            'domains': [
                (u'test.alexandra.network.lan', u'whatever'),
                (u'whatever.alexandra.network.lan', u'test'),
                (u'\u4f60\u597d.alexandra.network.lan', u'Ni Hao'),
                ],
            'entries': [
                # Title, entry, slug, user, tags, published
                (u'one', u'Post number 1', 'one', 1, ["c++", "c"], u'test', True),
                (u'two', u'Post number 2', 'two', 1, ["database", "testing"], u'test', True),
                (u'three', u'Post number 3', 'three', 1, ["c++", "database"], u'whatever', True),
                (u'four', u'Post number 4', 'four', 1, ["testing", "c"], u'whatever', True),
                (u'five', u'Post number 5', 'five', 1, ["c++", "c", "database"], u'test', True),
                (u'No tags', u'This post has no tags', 'no-tags', 1, [], u'whatever', True),
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
                user = User(email=u, name=r, credentials=c)
                DBSession.add(user)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print u'Username "{}" already exists.'.format(u)

        for (t, d) in defaults['tags']:
            sp = transaction.savepoint()
            try:
                tag = Tag(tag = t, description = d)
                DBSession.add(tag)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print u'Tag "{}" already exists.'.format(t)

        for (t, i, tag, o) in defaults['sites']:
            sp = transaction.savepoint()
            try:
                site = Site(title = t, idna = i, tagline = tag, owner =
                        DBSession.query(User).filter(User.email ==
                            o).first())
                DBSession.add(site)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print u'Site "{}" already exists.'.format(t)

        for (d, s) in defaults['domains']:
            sp = transaction.savepoint()
            try:
                domain = Domain(domain = d, site =
                        DBSession.query(Site).filter(Site.title == s).first())
                DBSession.add(domain)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print u'Domain "{}" already exists.'.format(d)

        for (t, e, s, u, ta, d, p) in defaults['entries']:
            sp = transaction.savepoint()
            try:
                insert_new_rev_entry(t, e, s, u, ta, d, published=p)
            except IntegrityError:
                sp.rollback()
                print u'Entry "{}" already exists.'.format(t)


def insert_new_rev_entry(title, entry, slug, user, tags, site, published=False):
    revision = Revision()
    revision.revision = 0
    revision.user_id = user
    revision.title = title
    revision.entry = entry

    for tag in tags:
        revision.tags.append(DBSession.query(Tag).filter(Tag.tag == tag).first())

    DBSession.add(revision)
    DBSession.flush()

    entry = Entry(current_rev = revision.id, slug = slug, site =
            DBSession.query(Site).filter(Site.title == site).first())
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
