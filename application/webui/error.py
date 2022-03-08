from flask import render_template

def error_not_found(_e):
    title = '404 - not found'

    return render_template(
        'error.html',
        title=title,
        heading='Oops, page not found!',
    ), 404
