#!/bin/bash
FLASK_PORT=5000

# Workers should be 2-4 per core in the server
WORKERS=2
MODULE_NAME=webui

# Logs
LOG_DIR=data/log
ACCESS_LOG_FILE=${LOG_DIR}/application_access.log
ERROR_LOG_FILE=${LOG_DIR}/application_error.log
ACCESS_LOG_FMT='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

mkdir -p ${LOG_DIR}

exec gunicorn \
    --bind :${FLASK_PORT} \
    --workers=${WORKERS} \
    --log-level=${LOG_LEVEL} \
    --access-logfile ${ACCESS_LOG_FILE} \
    --error-logfile ${ERROR_LOG_FILE} \
    --access-logformat="${ACCESS_LOG_FMT}" \
    ${RELOAD_ARG} \
    "${MODULE_NAME}:create_app(\"${CONFIG_STRATEGY}\", logger=\"gunicorn.error\")"
