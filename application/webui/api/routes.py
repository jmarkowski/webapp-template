from flask import Blueprint
from flask import current_app
from flask import jsonify

from webui.helpers import get_interactor


api_bp = Blueprint('api', __name__)


@api_bp.route('/api/config/<config_var>', methods=['GET'])
def config(config_var='TESTING'):
    config_var = config_var.upper()

    if config_var in current_app.config:
        config_dct = {config_var.lower(): current_app.config[config_var]}
    else:
        config_dct = {config_var.lower(): None}

    return jsonify(config_dct)


@api_bp.route('/api/invites', methods=['GET'])
def invites():
    i = get_interactor()
    email_lst = i.invitation.get_invite_list()

    invite_dct = {'emails': email_lst}

    current_app.logger.info(f'Fetched invite list: {email_lst}')

    return jsonify(invite_dct)
