import os

from flask import Flask
from webapp.main import main_bp
from config import config_map


def create_app(app_config, override_settings=None):
    """
    Create a Flask application using the factory pattern.
    """
    secrets_path = os.path.abspath('./secrets')
    app = Flask(__name__,
                instance_path=secrets_path,
                instance_relative_config=True,
                template_folder='views')

    app.config.from_object(config_map[app_config])

    # Load instance-specific overrides to the default configuration settings
    # that have been loaded above from an object.
    #
    # With `silent=True`, Flask will not crash if the `settings.py` file
    # does not exist.
    app.config.from_pyfile('settings.py', silent=True)

    if override_settings:
        app.config.update(override_settings)

    app.register_blueprint(main_bp)

    return app
