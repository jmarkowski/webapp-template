from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request

from core.gateway import InvitationDataGateway
from core.interactor import InvitationInteractor
from util.datetime import now_str
from util.email import InvalidEmail
from util.email import parse_email


main_bp = Blueprint('main', __name__)


def get_invitation_interactor():
    gateway = InvitationDataGateway(current_app.db)
    logger = current_app.logger
    return InvitationInteractor(gateway, logger)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    heading = 'Web Application Template'
    leading_text = 'This barebones HTML document is served from a dynamic ' \
                   'python backend.'

    email = request.form.get('email')
    already_invited = False
    is_email_valid = False

    try:
        is_email_valid = True if parse_email(email) else False

        interactor = get_invitation_interactor()

        if interactor.is_email_already_invited(email):
            already_invited = True
        else:
            interactor.add_email_to_invite_list(email)
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
    interactor = get_invitation_interactor()
    email_lst = interactor.get_invite_list()

    invite_dct = {'emails': email_lst}

    current_app.logger.info(f'Fetched invite list: {email_lst}')

    return jsonify(invite_dct)


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
        'time_now': now_str
    }
