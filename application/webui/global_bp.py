from flask import Blueprint
from flask import current_app

from util.datetime import now_str


global_bp = Blueprint('global', __name__)


@global_bp.app_context_processor
def util_processor():
    """Inject the following dictionary into all templates and render them
    automatically.
    """
    info = current_app.config['INFO']
    debug = current_app.config['DEBUG']

    return {
        'debug': debug,
        'info': info,
        'time_now': now_str
    }
