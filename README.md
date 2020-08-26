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

Currently, the `.env` file expects the following data to be configured:

    ```
    WEBAPP=webapp
    HOST_HTTP_PORT=8000
    HOST_SQL_ADMIN_PORT=8080

    # Configure the application environment context.
    # Options:
    #   development
    #   production
    #   testing
    APP_CONFIG=development

    # Add the following prefix to all images built with docker-compose
    COMPOSE_PROJECT_NAME=${WEBAPP}
    ```

For more information on defining environment variables, see
[https://docs.docker.com/compose/env-file/](https://docs.docker.com/compose/env-file/)

### Changing the Container Prefixes

To change the container prefixes (by default they are `webapp_*`), you will need
to modify two files prior to running the docker-compose command:

*  `./.env`
    * Set the `WEBAPP` variable, which will be the container prefix.
*  `./reverse-proxy/nginx.conf`
    * Change references to `webapp_*` to match the new container prefix.
    * Unfortunately, nginx does not have a simple and elegant way to pass
      environment variables into their configuration file.


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

        $ ./command app shell

2. As a command executed in the application container.

        $ docker-compose exec application bash
        # flask shell

The interactive shell will expose variables that may define within the
`application/main.py` file.

See the [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/cli/#open-a-shell)
for more details.


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
