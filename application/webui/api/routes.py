import html

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request

from webui.helpers import get_interactor
from util.email import InvalidEmail
from util.email import parse_email
from util.email import send_email


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


@api_bp.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()

    response = {
        'success': False
    }

    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not name:
        response['error'] = 'The name field is missing.'
        return jsonify(response)

    if not email:
        response['error'] = 'The email is missing.'
        return jsonify(response)

    if not subject:
        response['error'] = 'The subject is missing.'
        return jsonify(response)

    if not message:
        response['error'] = 'There is nothing in the message body.'
        return jsonify(response)

    email_tokens = None

    try:
        email_tokens = parse_email(email)
    except InvalidEmail:
        response['error'] = f'Oops, {email} appears to be an invalid email.'
        return jsonify(response)

    if email_tokens:
        message = html.escape(message) # Remove possible tags in the email
        message = message.replace('\n', '<br>') # New lines

        product = current_app.config['INFO']['product']

        subject = f'[{product}] {subject}'
        body = f"""
<!DOCTYPE html>
<html>
<body>
<em>From:</em> {name} (<a href="mailto:{email}">{email}</a>)
<br>
<em>Message:</em>
<br><br>
{message}
</body>
</html>
"""
        email_sent = send_email(subject, body, current_app.config)

        if not email_sent:
            response['error'] = 'Sorry, due to technical ' \
                'difficulties we were unable to forward your message ' \
                'at this time. '

        response['success'] = True

    return jsonify(response)
