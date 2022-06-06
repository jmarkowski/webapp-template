from flask import Blueprint
from flask import render_template


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    # Templates are searched globally, first at the application level, and then
    # at the blueprint level.
    return render_template(
        'index.html',
    )
