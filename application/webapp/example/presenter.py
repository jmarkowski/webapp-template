from flask import Blueprint
from flask import current_app
from flask import jsonify


page = Blueprint('page', __name__, template_folder='views')


@page.route('/')
def index():
    return 'Hello World!'


@page.route('/config/<config_var>', methods=['GET'])
def config(config_var='TESTING'):
    config_var = config_var.upper()

    if config_var in current_app.config:
        config_dct = {config_var.lower(): current_app.config[config_var]}
    else:
        config_dct = {config_var.lower(): None}

    return jsonify(config_dct)
