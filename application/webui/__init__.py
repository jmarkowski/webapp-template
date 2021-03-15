import logging
import os
from time import sleep

from flask import Flask
from flask import _app_ctx_stack

from config import create_config
from core.database import init_db_session
from core.database import deinit_db_session
from webui.error import error_not_found
from util import abort


def init_blueprints(app):
    # Import the blueprints only as they are needed (this prevents circular
    # dependencies).
    from webui.main import main_bp
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


def create_app(config_strategy, override_settings=None, logger=None):
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__, template_folder='views')

    if config_strategy is None:
        abort('Configuration strategy not specified.')

    if logger:
        logger_ = logging.getLogger(logger)
        app.logger.handlers = logger_.handlers
        app.logger.setLevel(logger_.level)

        app.logger.info(f'Using logger: {logger}')
    else:
        logging_map = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        logging_level = logging_map[os.getenv('LOG_LEVEL', 'debug')]
        app.logger.setLevel(logging_level)

        app.logger.info('No logger specified, streaming logs to output.')

    cfg = create_config(config_strategy=config_strategy,
                        override_settings=override_settings)
    app.config.from_object(cfg)

    init_blueprints(app)
    init_extensions(app)
    init_error_handlers(app)
    init_db(app)

    return app
