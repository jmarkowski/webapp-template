from flask import Blueprint
from flask import current_app
from flask import jsonify


main_bp = Blueprint('main_bp', __name__, template_folder='views')


@main_bp.route('/')
def index():
    return 'Hello World!'


@main_bp.route('/config/<config_var>', methods=['GET'])
def config(config_var='TESTING'):
    config_var = config_var.upper()

    if config_var in current_app.config:
        config_dct = {config_var.lower(): current_app.config[config_var]}
    else:
        config_dct = {config_var.lower(): None}

    return jsonify(config_dct)
