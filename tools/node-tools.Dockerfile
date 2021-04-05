FROM node:15.13.0-buster

RUN set -x \
    && apt-get update

ARG HOME=/home/node

WORKDIR ${HOME}

# SASS
ARG SASS_VERSION=1.30.0
COPY download/dart-sass/dart-sass-${SASS_VERSION}-linux-x64.tar.gz .
RUN tar xvf *.tar.gz && rm -f *.tar.gz
ENV PATH=$PATH:${HOME}/dart-sass

# Autoprefixer (required by Bootstrap 4)
ARG AUTOPREFIXER_VERSION=10.1.0
COPY download/autoprefixer/${AUTOPREFIXER_VERSION}.tar.gz .
RUN tar xvf *.tar.gz && rm -f *.tar.gz
ENV PATH=$PATH:${HOME}/autoprefixer-${AUTOPREFIXER_VERSION}/bin

# UglifyJS
ARG UGLIFYJS_VERSION=3.13.3
COPY download/uglifyjs/v${UGLIFYJS_VERSION}.tar.gz .
RUN tar xvf *.tar.gz && rm -f *.tar.gz
ENV PATH=$PATH:${HOME}/UglifyJS-${UGLIFYJS_VERSION}/bin
