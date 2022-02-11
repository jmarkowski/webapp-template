# Overview

This repository contains a boilerplate setup for a scalable python-based web
application using the Flask framework, an nginx reverse-proxy as the load
balancer, and PostgreSQL as the database along with a web-based database
administration portal.

The setup uses the production-grade [gunicorn](https://gunicorn.org/) WSGI HTTP
server to serve the Flask application, running in a python virtual environment.

It also uses [nginx](https://www.nginx.com/) to serve as a reverse-proxy
to achieve [layer 7 load balancing](https://www.nginx.com/resources/glossary/layer-7-load-balancing/).

Database interface support using an ORM is added using [SQLAlchemy](https://www.sqlalchemy.org).
The use of the [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy)
plugin is intentionally avoided to support Flask-decoupled testing of database.
In addition, it promotes a separation of concerns.
See [Use Flask and SQLAlchemy, not Flask-SQLAlchemy!](https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4)
for more details.

Database migration support was added using the [Alembic](https://alembic.sqlalchemy.org),
which is specifically intended for use in combination with SQLAlchemy.


# Project Initialization

## Initialize Submodules

This project incorporates and compiles changes that are dependent on other
subprojects. Once you've cloned this repository, the subprojects may be
initailized as follows:

    $ git submodule init
    $ git submodule update


## Configuration

The following commands will configure the template project with a custom project
name.

    $ ./configure --project=myproj
    $ make

For a set of configuration options, use the help flag: `./configure -h`.


## Install Tools

All tools are included in docker containers. These tools are executed from
within the docker container to compile sources.

To install the tools, move into the `tools` directory and run the script.

    $ cd tools/
    $ ./install-tools


## Compile Custom Theme

Under the `application/` directory is a `Makefile` that compiles a custom
bootstrap CSS from its source files and custom inputs. This file must be
compiled so that the page formatting from CSS is working.

    $ cd application/
    $ make


# Development With Docker

## Setup

By default, `docker compose` reads environment variables from a file named
`.env` in the same path as the `docker-compose.yaml` file, which orchestrates
and configures the execution of the various docker containers.

Included is a `.env` file with default values set. When the project is
initialized, the `.env` will be removed from the repository cache as it contains
sensitive settings.

For more information on defining environment variables, see
[https://docs.docker.com/compose/env-file/](https://docs.docker.com/compose/env-file/)


## First Run

Run the following command as `docker-compose.yaml` to build the services:

    $ docker-compose build

Once the containers are built, it is recommended that the database be
initialized using alembic. However, if there are no alembic migrations
(i.e. no `application/alembic/versions` directory), then this step
may be skipped.

    $ ./command start maint

    webapp$ alembic upgrade head

    $ ./command stop

At this point, the database is initialized, so now you can run the following
command to create and start the docker containers:

    $ docker-compose up

(You may optionally run `docker-compose up --build` to achieve the same result
as above in one step)

At this point, you may access the base application from the browser

    http://localhost:8000

To stop the service, hit `Ctrl-c` from the docker container.

When the docker container runs, it mounts the `application` directory on your
host machine as a volume within the docker container.

The gunicorn server is configured to automatically reload the application if it
detects any changes allowing your modifications to the application to take
effect immediately.

This is made possible from `RELOAD_ARG` in the `docker-compose.yaml` file.


## Administering the SQL Database

You can administer the SQL database by accessing the following address in your
browser:

    http://localhost:8080

The web-based administration server is being hosted by the `sql_administration`
docker container.

Using the information in the `.env` file, enter the following information to log
in:

    System:   PostgreSQL
    Server:   <SQL_DATABASE_SERVER_NAME>
    Username: <POSTGRES_USER>
    Password: <POSTGRES_PASSWORD>
    Database: <POSTGRES_DB>


## Working in a Flask Shell

With the containers running, there are a couple of ways you can start working
within the flask shell:

* Using the top-level `command` script.

        $ ./command app flask shell

* As a command executed in the application container.

        $ docker-compose exec application bash
        # flask shell

The interactive shell will expose variables that may define within the
`application/main.py` file.

See the [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/cli/#open-a-shell)
for more details.


## Working with Alembic

When working with alembic, you will need to initialize all of the services in
maintenance mode. In this mode, all of the services will run except for the main
application.

    $ ./command start maint

This will automatically start the bash terminal in the root of the application.
From here, you can run alembic commands.

    # alembic

See the `application/README.md` for a quick summary of how to work with database
migrations using Alembic.

Conventiently, at the same time you may access `http://localhost:8080` to
administer the SQL database.

When you are finished working in this environment, type `exit` or hit `CTRL+D`
to stop the running containers:

    $ ./command stop


## Modifying the Application's Dockerfile

1. Make the required changes to `application/Dockerfile`.

2. Bump the `application` (and possibly the `email_notifier`) service version
   tag using semantic versioning.

   For example, if the changes could host previous versions of the
   application, bump the minor version. This is an appropriate upgrade path if
   the changes do not require changes to the application code.
   i.e. `application:1.0` -> `application:1.1`

   However, if the Dockerfile changes require changes to the application code,
   then a major version bump is required.
   i.e. `application:1.0` -> `appplication:2.0`

3. Change any other references of the old image version to the new one
   (e.g. `command`)

4. Starting the application should create the new docker images.


# Unit Testing the Application

With the containers running, there are a few ways you can run the unit tests:

* Using the top-level `command` script.

        $ ./command app test

* As a one-liner bash command executed in the application container.

        $ docker-compose exec application bash -c "ls -1 tests/*.py | xargs -I{} python3 {}"

* One at a time through an interactive bash shell in the application container.

        $ docker-compose exec application bash
        # python3 -m tests.example


# Development Without Docker

If, for whatever reason, you're interested in developing the python-based
application without having to run docker services, you may do so as described
below.

However, note that this approach should only be used for development purposes
only, and is not a robust solution for a hosting your application in a
production environment as any database changes will *not* be persistent!

1. Create a virtual python environment and install the dependencies.

        $ cd application
        $ python -m venv pyenv
        $ ./pyenv/bin/pip install -r requirements.txt

2. Initialize the environment.

        $ source pyenv/bin/activate

3. Start the application with flask, specifying the various required
   environment settings.

   There are many supported ways of running the application.

   a) Run it using the flask application.

        $ FLASK_APP=main.py FLASK_RUN_PORT=8000 FLASK_DEBUG=1 flask run

   b) Run it using the python interpreter.

        $ FLASK_RUN_PORT=8000 FLASK_DEBUG=1 python -m main

   c) Run it using the application defaults.

        $ python -m main

   d) Run it by simply executing main.py.

        $ ./main.py

4. Access the application from the browser.

        http://localhost:8000
