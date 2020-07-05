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


# Development With Docker

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


## Environment Configuration

The `docker-compose.yaml` file reads environment variables that are defined in
a `.env` file at the same location.

The `.env` file expects the following data to be configured:

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

See https://docs.docker.com/compose/env-file/


## Changing the Application Name

By default, `docker-compose.yaml` uses an environment file named `.env` in the
same directory as it.

That file should specify the `WEBAPP` environment variable with the name of the
application.

Note that this will change the application container (default:
`webapp_container`), which means you will need to update
`reverse-proxy/nginx.conf` to specify the new container name.


## Changing the Container Name

To change the container names so that they are not simply `webapp_applicaton`
and `webapp_proxy`, you will need to make changes to two files:

*  `./docker-compose.yaml`
*  `./reverse-proxy/nginx.conf`

Only within these files are the container names referenced.


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

With the containers running, connect to the application:

    $ docker-compose exec application bash

Finally, execute the test scripts:

    $ python3 tests/*.py

Note: Alternatively, you may want to opt for running the tests according to the
module name. For example,

    $ python3 -m tests.example


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
