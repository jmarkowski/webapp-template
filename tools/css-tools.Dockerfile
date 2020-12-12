FROM node:15.4.0-buster

RUN set -x \
    && apt-get update

ARG SASS_VERSION=1.30.0
ARG AUTOPREFIXER_VERSION=10.1.0
ARG HOME=/home/node

WORKDIR ${HOME}

# SASS
RUN wget https://github.com/sass/dart-sass/releases/download/${SASS_VERSION}/dart-sass-${SASS_VERSION}-linux-x64.tar.gz
RUN tar xvf *.tar.gz && rm -f *.tar.gz
ENV PATH=$PATH:${HOME}/dart-sass

# Autoprefixer (required by Bootstrap 4)
RUN wget https://github.com/postcss/autoprefixer/archive/${AUTOPREFIXER_VERSION}.tar.gz
RUN tar xvf *.tar.gz && rm -f *.tar.gz
ENV PATH=$PATH:${HOME}/autoprefixer-${AUTOPREFIXER_VERSION}/bin
