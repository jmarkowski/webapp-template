# Overview

This repository contains a boilerplate setup for a scalable python-based web
application using the Flask framework and an nginx reverse-proxy as the load
balancer.

The setup uses the production-grade [gunicorn](https://gunicorn.org/) WSGI HTTP
server to serve the Flask application, running in a python virtual environment.

It also uses [nginx](https://www.nginx.com/) to serve as a reverse-proxy
to achieve [layer 7 load balancing](https://www.nginx.com/resources/glossary/layer-7-load-balancing/).

As such, this repository contains two docker images: one for the application and
one for the load balancer.


# Project Initialization

Included in this repository is an `init` script that removes files that should
not be committed as part of your project.

It's expected that if you're initializing the project for the first time, you'll
run the script.

    $ ./init


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
    Server: webapp_sql_database
    Username: <./secrets/postgres_user.txt>
    Password: <./secrets/postgres_password.txt>
    Database: webapp_db


## Working in a Flask Shell

With the containers running, connect to the application:

    $ docker-compose exec application bash

From here, you can launch the Flask shell as follows:

    $ flask shell

This interactive shell will expose variables that may define within the
`application/main.py` file.

See the [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/cli/#open-a-shell)
for more details.


# Unit Testing the Application

With the containers running, you may execute all of the tests as follows:

    $ docker-compose exec application bash -c "ls -1 tests/*.py | xargs -I{} python3 {}"

Note: Alternatively, you may want to opt for running the tests according to the
module name. However, you would only be able to do this indivually. For example,

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


# Starting Your Own Project

1. Copy this project, or add it as an upstream source.
2. Create your feature branch from this repository's master.
3. Delete the files and folders (and add your own but *do not version control it*)
    - `.env`
    - `secrets/*`
    - `application/secrets/settings.py`
4. Commit your changes to your project repository, push, merge.
5. The rest is all up to you.


# Wish List

* Makefile based, with settings that can be used to fetch and install various
  frameworks (for example, bootstrap, and fontawesome)
