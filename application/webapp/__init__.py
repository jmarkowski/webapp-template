from flask import Flask
from webapp.main import main_bp
from config import config_map


def create_app(app_config, override_settings=None):
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__)

    app.config.from_object(config_map[app_config])

    if override_settings:
        app.config.update(override_settings)

    app.register_blueprint(main_bp)

    return app
