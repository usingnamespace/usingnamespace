import os
import sys
import transaction
import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from sqlalchemy.exc import IntegrityError

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from .. import models as m

defaults = {
    'users': [
        (u'xistence@0x58.com', u'Bert JW Regeer', 'test'),
        (u'test@0x58.com', u'Test Testing', 'test'),
        ],
    'sites': [
        (u'whatever', u'Everything and anything', "xistence@0x58.com"),
        (u'test', u'A simple test', "xistence@0x58.com"),
        (u'howdy', u'Another very simple test', "xistence@0x58.com"),
        (u'\u4f60\u597d', u'A blog detailing my ventures in China', "xistence@0x58.com"),
        (u'howdy', u'Another very simple test', "test@0x58.com"),
        ],
    'tags': [
        (u'c++', "The C++ programming language"),
        (u'c', "The C progrmaming langauge"),
        (u'database', "Databases store stuff"),
        (u'testing', "Not sure..."),
        (u'not used', "Don't look at me that way"),
        ],
    'domains': [
        (u'test.alexandra.network.lan', u'whatever', "xistence@0x58.com"),
        (u'whatever.alexandra.network.lan', u'test', "xistence@0x58.com"),
        (u'\u4f60\u597d.alexandra.network.lan', u'\u4f60\u597d', "xistence@0x58.com"),
        (u'test.sterling.local', u'whatever', "xistence@0x58.com"),
        (u'test2.sterling.local', u'test', "xistence@0x58.com"),
        (u'test3.sterling.local', u'\u4f60\u597d', "xistence@0x58.com"),
        (u'howdy.alexandra.network.lan', u'howdy', "test@0x58.com"),
        ],
    'entries': [
        # Title, entry, slug, user, tags, published
        (u'one', u'Post number 1', 'one', u'xistence@0x58.com', ["c++", "c"], u'test', True),
        (u'two', u'Post number 2', 'two', u'xistence@0x58.com', ["database", "testing"], u'test', True),
        (u'three', u'Post number 3', 'three', u'xistence@0x58.com', ["c++", "database"], u'whatever', True),
        (u'four', u'Post number 4', 'four', u'xistence@0x58.com', ["testing", "c"], u'whatever', True),
        (u'five', u'Post number 5', 'five', u'xistence@0x58.com', ["c++", "c", "database"], u'test', True),
        (u'No tags', u'This post has no tags', 'no-tags', u'xistence@0x58.com', [], u'whatever', True),
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
    # Remove this later when you are no longer using PasteDeploy
    global_conf = settings.global_conf
    global_conf.update(settings)

    settings = global_conf

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        DBSession = get_tm_session(session_factory, transaction.manager)

        for (u, r, c) in defaults['users']:
            sp = transaction.savepoint()
            try:
                user = m.User(email=u, name=r, credentials=c)
                DBSession.add(user)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print(u'Username "{}" already exists.'.format(u))

        for (t, tag, o) in defaults['sites']:
            sp = transaction.savepoint()
            try:
                site = (
                    m.Site(
                        title=t,
                        tagline=tag,
                        owner=(
                            DBSession
                            .query(m.User)
                            .filter(m.User.email == o)
                            .first()
                        )
                    )
                )
                DBSession.add(site)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print(u'Site "{}" already exists.'.format(t))

        for (t, d) in defaults['tags']:
            sp = transaction.savepoint()
            try:
                for (s, _, o) in defaults['sites']:
                    owner = DBSession.query(m.User).filter(m.User.email == o).first()
                    site = (
                        DBSession
                        .query(m.Site)
                        .filter(m.Site.title == s)
                        .filter(m.Site.owner == owner)
                        .first()
                    )

                    if site is None:
                        raise RuntimeError("Site doesn't exist. Bailing.")

                    tag = m.Tag(tag=t, description=d, site=site)
                    DBSession.add(tag)
                    DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print(u'Tag "{}" already exists.'.format(t))

        for (d, s, o) in defaults['domains']:
            sp = transaction.savepoint()
            try:
                owner = DBSession.query(m.User).filter(m.User.email == o).first()
                site = (
                    DBSession
                    .query(m.Site)
                    .filter(m.Site.title == s)
                    .filter(m.Site.owner == owner)
                    .first()
                )
                domain = m.Domain(domain=d, site=site)
                DBSession.add(domain)
                DBSession.flush()
            except IntegrityError:
                sp.rollback()
                print(u'Domain "{}" already exists.'.format(d))

        for (t, e, s, u, ta, d, p) in defaults['entries']:
            sp = transaction.savepoint()
            try:
                insert_new_rev_entry(t, e, s, u, ta, d, DBSession, published=p)
            except IntegrityError:
                sp.rollback()
                print(u'Entry "{}" already exists.'.format(t))


def insert_new_rev_entry(
    title,
    entry,
    slug,
    user,
    tags,
    site,
    DBSession,
    published=False
):
    revision = m.Revision()
    revision.revision = 0
    revision.author = (
        DBSession
        .query(m.User)
        .filter(m.User.email == user)
        .first()
    )
    revision.title = title
    revision.entry = entry

    site = (
        DBSession
        .query(m.Site)
        .filter(m.Site.title == site)
        .first()
    )

    for tag in tags:
        tag_db = (
            DBSession
            .query(m.Tag)
            .filter(m.Tag.tag == tag)
            .filter(m.Tag.site == site)
            .first()
        )
        revision.tags.append(tag_db)

    DBSession.add(revision)
    DBSession.flush()

    entry = m.Entry(
        current_rev=revision.id,
        slug=slug,
        site=site
    )
    if published:
        entry.pubdate = datetime.datetime.now()

    DBSession.add(entry)
    DBSession.flush()

    author = m.EntryAuthors()
    author.entry_id = entry.id
    author.user_id = user
    author.revision_id = revision.id

    DBSession.add(entry)
    DBSession.flush()
