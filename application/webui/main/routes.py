from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request

from util.email import InvalidEmail
from util.email import parse_email
from webui.helpers import get_interactor


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    heading = 'Web Application Template'
    leading_text = 'This barebones HTML document is served from a dynamic ' \
                   'python backend.'

    email = request.form.get('email')
    already_invited = False
    is_email_valid = False

    try:
        is_email_valid = bool(parse_email(email))

        i = get_interactor()

        if i.invitation.is_email_already_invited(email):
            already_invited = True
        else:
            i.invitation.add_email_to_invite_list(email)
    except InvalidEmail:
        pass

    # Templates are searched globally, first at the application level, and then
    # at the blueprint level. For this reason, we "namespace" our
    # blueprint-specific templates by prefixing them with the blueprint name.
    return render_template('main/index.html',
                           heading=heading,
                           leading_text=leading_text,
                           email=email,
                           is_email_valid=is_email_valid,
                           already_invited=already_invited)


@main_bp.route('/config/<config_var>', methods=['GET'])
def config(config_var='TESTING'):
    config_var = config_var.upper()

    if config_var in current_app.config:
        config_dct = {config_var.lower(): current_app.config[config_var]}
    else:
        config_dct = {config_var.lower(): None}

    return jsonify(config_dct)


@main_bp.route('/invites', methods=['GET'])
def invites():
    i = get_interactor()
    email_lst = i.invitation.get_invite_list()

    invite_dct = {'emails': email_lst}

    current_app.logger.info(f'Fetched invite list: {email_lst}')

    return jsonify(invite_dct)
