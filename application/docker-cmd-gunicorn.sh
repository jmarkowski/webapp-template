#!/bin/bash
FLASK_PORT=5000

# Workers should be 2-4 per core in the server
WORKERS=2
MODULE_NAME=webapp

exec gunicorn \
    --bind :${FLASK_PORT} \
    --workers=${WORKERS} \
    --access-logfile - \
    --error-logfile - \
    ${RELOAD_ARG} \
    "${MODULE_NAME}:create_app(\"${APP_CONFIG}\")"
