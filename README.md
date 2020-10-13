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

The following commands will configure the template project.

    $ ./configure
    $ make

For a set of configuration options, use the help flag: `./configure -h`.


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

### Changing the Container Prefixes

To change the container prefixes (by default they are `webapp_*`), you will need
to change the `webapp_*` references in the following two files prior to running
th containeres:

* `./.env`
* `./reverse-proxy/nginx.conf`


## First Run

Run the following command as `docker-compose.yaml` to build the services:

    $ docker-compose build

And now run the following to create and start the docker containers:

    $ docker-compose up

You may optionally run the following to achieve the same result as above:

    $ docker-compose up --build

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

Use the following information to log in:

    System: PostgreSQL
    Server: sql_database
    Username: <./secrets/postgres_user.txt>
    Password: <./secrets/postgres_password.txt>
    Database: webapp_db


## Working in a Flask Shell

With the containers running, there are a couple of ways you can start working
within the flask shell:

1. Using the top-level `command` script.

        $ ./command app flask shell

2. As a command executed in the application container.

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


# Unit Testing the Application

With the containers running, there are three ways you can run the unit tests:

1. Using the top-level `command` script.

        $ ./command app test

2. As a one-liner bash command executed in the application container.

        $ docker-compose exec application bash -c "ls -1 tests/*.py | xargs -I{} python3 {}"

3. One at a time through an interactive bash shell in the application container.

        $ docker-compose exec application bash
        # python3 -m tests.example


# Development Without Docker

These are the instructions for developing the python application in the
recommended old-school Flask fashion without the docker services.

This approach is for development only, and is not a viable solution for a production
environment!

1.  Initialize the environment

        $ cd application
        $ python -m venv pyenv
        $ ./pyenv/bin/pip install -r requirements.txt

2.  Start the environment

        $ source pyenv/bin/activate
        $ export FLASK_APP=main.py
        $ export FLASK_DEBUG=1

3.  Start the application with flask

        $ flask run

4.  Access the application from the browser

        http://localhost:5000
