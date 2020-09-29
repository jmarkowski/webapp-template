import os
from time import sleep

from flask import Flask
from flask import _app_ctx_stack

from config import config_map
from core.database import init_db_session
from core.database import deinit_db_session
from webapp.error import error_not_found


def init_blueprints(app):
    # Import the blueprints only as they are needed (this prevents circular
    # dependencies).
    from webapp.main import main_bp
    app.register_blueprint(main_bp)


def init_extensions(app):
    # Any plug-in Flask extensions that require initialization may be done here.
    pass

def init_error_handlers(app):
    app.register_error_handler(404, error_not_found)


def init_db(app):
    db_uri = app.config.get('DB_URI')

    db_ready = False
    retry_interval_s = 5

    # The database connection MUST be available for the service to run.
    while not db_ready:
        try:
            app.db = init_db_session(db_uri, \
                scopefunc=_app_ctx_stack.__ident_func__,
                echo_raw_sql=app.config.get('DEBUG'))

            # Register a function to close the database session when the
            # application context is popped.
            @app.teardown_appcontext
            def close_db_session(app):
                from flask import current_app
                deinit_db_session(current_app.db)

            db_ready = True
        except Exception as e:
            print('Failed to connect to DB_URI \'{}\': {}'.format(db_uri, e))
            sleep(retry_interval_s)


def create_app(app_config, override_settings=None):
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__, template_folder='views')

    cfg = config_map[app_config](override_settings=override_settings)
    app.config.from_object(cfg)

    init_blueprints(app)
    init_extensions(app)
    init_error_handlers(app)
    init_db(app)

    return app
