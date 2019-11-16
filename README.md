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


# Launching the Services

Run the following command as `docker-compose.yml` to build the services:

    $ docker-compose build

And now run the following to create and start the docker containers:

    $ docker-compose up

You may optionally run the following to achieve the same result as above:

    $ docker-compose up --build

At this point, you may access the base application from the browser

    http://localhost:8000

To stop the service, hit `Ctrl-c` from the docker container.


# Updating Your Application

If you make any changes to the application, you'll need to rebuild the images
when launching.

    $ docker-compose up --build


# Developing for the Application

Follow these instructions to launch the application in Flask (not gunicorn).

This is for development only, and is not a viable solution for a production
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
