from flask import Blueprint
from flask import current_app


page = Blueprint('page', __name__, template_folder='views')


@page.route('/')
def index():
    debug_state = 'enabled' if current_app.config['DEBUG'] else 'disabled'
    return 'Hello World! (debug_state = {})'.format(debug_state)
