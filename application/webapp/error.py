from flask import abort
from flask import current_app
from flask import render_template

def error_not_found(e):
    return render_template('error.html', error='404',
                           heading='Oops, page not found!'), 404
