from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template


main_bp = Blueprint('main_bp', __name__, template_folder='views')


@main_bp.route('/')
def index():
    title = 'Web Application Template'
    heading = 'Heading'
    text = 'Text'

    # Templates are searched globally, first at the application level, and then
    # at the blueprint level. For this reason, we "namespace" our
    # blueprint-specific templates by prefixing them with the blueprint name.
    return render_template('main_index.html',
                           title=title,
                           heading=heading,
                           text=text)


@main_bp.route('/config/<config_var>', methods=['GET'])
def config(config_var='TESTING'):
    config_var = config_var.upper()

    if config_var in current_app.config:
        config_dct = {config_var.lower(): current_app.config[config_var]}
    else:
        config_dct = {config_var.lower(): None}

    return jsonify(config_dct)
