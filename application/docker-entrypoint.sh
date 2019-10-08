#!/bin/bash
FLASK_PORT=5000

# Workers should be 2-4 per core in the server
WORKERS=2
MODULE_NAME=webapp
VARIABLE_NAME=app

exec gunicorn \
    --bind :${FLASK_PORT} \
    --workers=${WORKERS} \
    --access-logfile - \
    --error-logfile - \
    ${MODULE_NAME}:${VARIABLE_NAME}
