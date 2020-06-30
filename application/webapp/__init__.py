from flask import Flask
from webapp.example import page


def create_app(override_settings=None):
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__)

    app.config.from_object('config.settings')

    if override_settings:
        app.config.update(override_settings)

    app.register_blueprint(page)

    return app
