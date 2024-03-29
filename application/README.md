# Compiling Frontend Sources

This directory contains a `Makefile` that transpiles and minifies the scripts
and styles found under the `static` directory into the `static/dist` folder.

To process the scripts and styles, simply execute the following instruction:

    $ make

NOTE: The node modules must be first install in order for this to successfully
run:

    $ make install

## Custom Theming

To customize the components that you would use for bootstrap, modify the
`scss/bootstrap.scss` file.

See [Customize SASS](https://getbootstrap.com/docs/5.1/customize/sass/)
for more details.


# Logs

The application is configured to generate persistent logs using the gunicorn
logger.

The logs are made available under the `data/log` directory.


# Database Migrations

`alembic` is a tool that interfaces with SQLAlchemy to support database
migrations (i.e. tracking changes made to various tables).

## Initial Alembic Setup

The following command was run to initialize the `alembic` setup:

    `alembic init alembic`

After this, several changes were made to the `alembic/env.py` file as per the
online documentation.

After this, the database was completely cleared, and a baseline migration was
created.

    `alembic revision --autogenerate -m "baseline"`

## Working With Alembic

When you run the `alembic revision` commands, they will create a file under
`alembic/versions` which will contain the upgrade and downgrade instructions
required to move up or down in the database migrations.

The `alembic/env.py` file was modified to support automatic revision generation
with the following command:

    `alembic revision --autogenerate -m "message"`

These autogenerated files need to be manually inspected before they are
committed to the source code repository, and definitely before they are run on
the database!

If you're happy with the changes, add the version file to the source code
repository with the changes made to the model.

    `git add core/database.py`
    `git add alembic/versions/*.py`

Finally, you may apply the changes to the database:

    `alembic upgrade +1`

NOTE: Alembic will create a table in your database called `alembic_version` that
will simply track where in the history the current database is.

## Moving Migrations Up And Down

To move up a migration:

    `alembic upgrade +1`

To move down a migration

    `alembic downgrade -1`

To see where you are in history

    `alembic current`

Or to see the entire history

    `alembic history --verbose`
