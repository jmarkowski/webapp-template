FROM node:17.9.0-bullseye-slim

RUN set -x \
    && apt-get update

ARG HOME=/home/node

WORKDIR ${HOME}
