#!/usr/bin/env python
# This file is used to run the application with flask, not gunicorn, in a
# standalone environment for development and debugging.
import os

from flask import current_app

from webui import create_app


app = create_app(os.getenv('CONFIG_STRATEGY', 'testing'))


@app.shell_context_processor
def make_shell_context():
    # In the context dictionary, add variables that you would like to expose
    # into the shell context. e.g. {'db': db} to expose the database.
    context_dct = {
        'db': current_app.db
    }
    return context_dct


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=os.getenv('FLASK_RUN_PORT', '8000'),
            debug=os.getenv('FLASK_DEBUG', '1') == '1')
