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


## Changing the Container Name

To change the container names so that they are not simply `webapp_applicaton`
and `webapp_proxy`, you will need to make changes to two files:

*  `./docker-compose.yaml`
*  `./reverse-proxy/nginx.conf`

Only within these files are the container names referenced.


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


# Wish List

* Makefile based, with settings that can be used to fetch and install various
  frameworks (for example, bootstrap, and fontawesome)
