import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'SQLAlchemy',
    'pyramid',
    'pyramid_tm',
    'transaction',
    'waitress',
    'zope.sqlalchemy',

    'cryptacular',
    'deform',
    'misaka',
    'psycopg2',
    'pyramid_deform',
    'pyramid_mailer',
    'pyramid_mako',
    ]

tests_require = []

testing_requires =  tests_require + [
    'nose',
    'coverage',
    ]

develop_requires = [
    'pyramid_debugtoolbar',
    ]

setup(name='usingnamespace',
      version='0.0',
      description='usingnamespace',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Bert JW Regeer',
      author_email='bertjw@regeer.org',
      url='http://usingnamespace.com/',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='usingnamespace.tests',
      install_requires=requires,
      tests_require=tests_require,
      extras_require = {
          'develop': develop_requires,
          'testing': testing_requires,
          },
      entry_points="""\
      [paste.app_factory]
      main = usingnamespace:main
      api  = usingnamespace.api:main
      management = usingnamespace.management:main
      [console_scripts]
      usingnamespace_init_db = usingnamespace.scripts.initializedb:main
      usingnamespace_destroy_db = usingnamespace.scripts.destroydb:main
      """,
      )

