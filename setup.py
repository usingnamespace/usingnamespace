import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'cryptacular',
    'misaka',
    'psycopg2',
    'pygments',
    'pyramid',
    'pyramid_authsanity',
    'pyramid_mailer',
    'pyramid_mako',
    'pyramid_services',
    'pyramid_retry',
    'pyramid_tm',
    'sqlalchemy',
    'transaction',
    'waitress',
    'zope.sqlalchemy',
]

tests_require = []

testing_requires = tests_require + [
    'pytest',
    'pytest-cov',
    'coverage',
]

develop_requires = [
    'pyramid_debugtoolbar',
]

setup(
    name='usingnamespace',
    version='0.0',
    description='usingnamespace',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Bert JW Regeer',
    author_email='bertjw@regeer.org',
    url='http://usingnamespace.com/',
    keywords='web wsgi pylons pyramid blog',
    packages=find_packages('.', exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'develop': develop_requires,
        'testing': testing_requires,
    },
    entry_points={
        "paste.app_factory": [
            'main = usingnamespace:main',
            'api = usingnamespace:api',
        ],
        "console_scripts": [
            'usingnamespace_init_db = usingnamespace.scripts.initializedb:main',
            'usingnamespace_destroy_db = usingnamespace.scripts.destroydb:main',
        ],
    }
)
