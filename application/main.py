import os

from flask import current_app

from webapp import create_app


app = create_app(os.getenv('CONFIG_STRATEGY'))


@app.shell_context_processor
def make_shell_context():
    # In the context dictionary, add variables that you would like to expose
    # into the shell context. e.g. {'db': db} to expose the database.
    context_dct = {
        'db': current_app.db
    }
    return context_dct
