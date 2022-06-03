import os

from flask import Blueprint
from flask import current_app
from flask import send_from_directory

from util.datetime import now_str


global_bp = Blueprint('global', __name__)


@global_bp.route('/<path:file_path>')
def serve_file(file_path):
    full_path = os.path.join(current_app.config['FILE_DIR'], file_path)

    dir = os.path.dirname(full_path)
    filename = os.path.basename(full_path)

    return send_from_directory(dir, filename)


@global_bp.app_context_processor
def util_processor():
    """Inject the following dictionary into all templates and render them
    automatically.
    """
    info = current_app.config['INFO']
    debug = current_app.config['DEBUG']
    plugin = current_app.config['PAGE_PLUGIN']

    return {
        'debug': debug,
        'info': info,
        'time_now': now_str,
        'plugin': plugin,
    }
