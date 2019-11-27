from flask import Flask
from webapp.blueprints.example import page


def create_app():
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__)

    app.config.from_object('config.settings')

    app.register_blueprint(page)

    return app
