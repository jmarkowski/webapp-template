from flask import Flask


def create_app():
    """
    Create a Flask application using the factory pattern.
    """
    app = Flask(__name__)

    app.config.from_object('config.settings')

    @app.route('/')
    def index():
        debug_state = 'enabled' if app.config['DEBUG'] else 'disabled'
        return 'Hello World! (debug_state = {})'.format(debug_state)

    return app
