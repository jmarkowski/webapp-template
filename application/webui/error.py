from flask import render_template


def render_error(http_status_code, http_status_phrase):
    title = f'{http_status_code} - {http_status_phrase}'

    return render_template(
        'error.html',
        title=title,
        http_status_code=http_status_code,
        http_status_phrase=http_status_phrase,
    ), http_status_code


def error_not_found(_e):
    return render_error(404, 'Not Found')
