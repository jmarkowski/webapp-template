from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request

import util.time


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    heading = 'Web Application Template'
    leading_text = 'This barebones HTML document is served from a dynamic python backend.'

    email = request.form.get('email')

    # Templates are searched globally, first at the application level, and then
    # at the blueprint level. For this reason, we "namespace" our
    # blueprint-specific templates by prefixing them with the blueprint name.
    return render_template('main/index.html',
                           heading=heading,
                           leading_text=leading_text,
                           email=email)


@main_bp.route('/config/<config_var>', methods=['GET'])
def config(config_var='TESTING'):
    config_var = config_var.upper()

    if config_var in current_app.config:
        config_dct = {config_var.lower(): current_app.config[config_var]}
    else:
        config_dct = {config_var.lower(): None}

    return jsonify(config_dct)


# Note: We are using the `app_context_processor` to have these functions
# available globally.
@main_bp.app_context_processor
def util_processor():
    """Inject the following dictionary into all templates and render them
    automatically.
    """
    site = current_app.config['SITE']

    return {
        'site': site,
        'time_now': util.time.now
    }