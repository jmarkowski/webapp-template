from flask import render_template

def error_not_found(_e):
    return render_template('error.html', error='404',
                           heading='Oops, page not found!'), 404
