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

At this point, you may launch your browser and goto http://localhost:8000

To stop the service, hit `Ctrl-c`.


# Updating Your Application

If you make any changes to the application, you'll need to rebuild the images
when launching.

    $ docker-compose up --build
