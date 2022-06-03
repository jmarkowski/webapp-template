from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request

from util.email import InvalidEmail
from util.email import parse_email
from webui.helpers import get_interactor


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    title = 'Application Tagline'
    heading = current_app.config['INFO']['product']
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
    return render_template('index.html',
                           title=title,
                           heading=heading,
                           leading_text=leading_text,
                           email=email,
                           is_email_valid=is_email_valid,
                           already_invited=already_invited)
