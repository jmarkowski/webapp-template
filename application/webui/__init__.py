import logging
import os
from glob import glob
from time import sleep

from flask import Flask
from flask import current_app
from flask import _app_ctx_stack

from config import create_config
from core.dbgateway import DbGateway
from core.interactor import Interactor
from webui.error import error_not_found
from util import abort


def get_interactor():
    return Interactor(
        config=current_app.config['CONFIG'],
        db_gateway=DbGateway(current_app.db),
        logger=current_app.logger,
    )


def init_jinja_env(app):
    def glob_file_list(name_glob):
        root = current_app.static_folder
        return [f[len(root)+1:] for f in glob(os.path.join(root, name_glob))]

    app.jinja_env.globals.update(glob_file_list=glob_file_list)


def init_blueprints(app):
    # Import the blueprints only as they are needed (this prevents circular
    # dependencies).
    from webui.global_bp import global_bp
    app.register_blueprint(global_bp)

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
            app.db = DbGateway.open_session(db_uri, \
                scopefunc=_app_ctx_stack.__ident_func__,
                echo_raw_sql=app.config.get('DEBUG'))

            # Register a function to close the database session when the
            # application context is popped.
            @app.teardown_appcontext
            def close_db_session(app):
                DbGateway.close_session(current_app.db)

            db_ready = True
        except Exception as e:
            print('Failed to connect to DB_URI \'{}\': {}'.format(db_uri, e))
            sleep(retry_interval_s)


def create_app(config_strategy, override_settings=None, logger=None):
    """
    Create a Flask application using the factory pattern.
    """
    if config_strategy is None:
        abort('Configuration strategy not specified.')

    cfg = create_config(config_strategy=config_strategy,
                        override_settings=override_settings)

    app = Flask(__name__,
            static_folder=cfg.STATIC_DIR,
            template_folder=cfg.TEMPLATE_DIR)

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

    app.config.from_object(cfg)

    init_jinja_env(app)
    init_blueprints(app)
    init_extensions(app)
    init_error_handlers(app)
    init_db(app)

    return app
