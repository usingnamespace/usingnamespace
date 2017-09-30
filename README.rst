usingnamespace
==============

Installation
------------

Not available yet...

Developing
----------

Prerequisites:

 0. PostgreSQL 9.6, modify config/development.ini to configure the connection
    string
 1. Create new database for usingnamespace, and make sure to run as a database
    administrator in the new database:

    .. code::

        CREATE EXTENSION pgcrypto;

    This is used by the application to create UUID's.

    If PostgreSQL >9.4 is not available, you may also use the ``uuid-ossp`` extension:

    .. code::

        CREATE EXTENSION "uuid-ossp";

    Then add a new function:

    .. code::

        CREATE FUNCTION gen_random_uuid()
        RETURNS uuid
        AS '
        BEGIN
        RETURN uuid_generate_v4();
        END'
        LANGUAGE 'plpgsql';

 2. Yarn has to be installed (node as well...)

Getting the application set up locally:

 0. Change directory to this project
 1. Create virtualenv for Project in $venv
 2. $venv/bin/pip install -e .
 3. $venv/bin/usingnamespace_db_init config/development.ini
 4. cd webassets
    yarn install
 5. In a seperate terminal window:
    yarn run watch
 6. In a seperate terminal window:
    $venv/bin/pserve --reload config/development.ini
 7. Visit the URL printed on the console
