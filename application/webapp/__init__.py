import os

from flask import Flask
from flask import _app_ctx_stack

from config import config_map
from util.sqlalchemy import create_tables
from util.sqlalchemy import get_db_interface


secret_config = './secrets/settings.py'


def check_config_conditions(app):
    # Check the configuration for any possible show-stopping settings, and
    # provide helpful assertion messages if needed.
    assert app.config.get('SECRET_KEY'), \
        'Define SECRET_KEY in {}'.format(secret_config)


def init_blueprints(app):
    # Import the blueprints only as they are needed (this prevents circular
    # dependencies).
    from webapp.main import main_bp
    app.register_blueprint(main_bp)


def init_extensions(app):
    # Any plug-in Flask extensions that require initialization may be done here.
    pass


def init_db(app):
    app.session, engine = get_db_interface(scopefunc=_app_ctx_stack.__ident_func__)
    create_tables(engine)


def create_app(app_config, override_settings=None):
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__,
                instance_path=os.path.abspath(os.path.dirname(secret_config)),
                instance_relative_config=True,
                template_folder='views')

    app.config.from_object(config_map[app_config])

    # Load instance-specific overrides to the default configuration settings
    # that have been loaded above from an object.
    #
    # With `silent=True`, Flask will not crash if the `settings.py` file
    # does not exist.
    app.config.from_pyfile(os.path.basename(secret_config), silent=True)

    if override_settings:
        app.config.update(override_settings)

    check_config_conditions(app)

    init_blueprints(app)
    init_extensions(app)
    init_db(app)

    return app
