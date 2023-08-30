from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response


def token_missing():
    response = api_abort(401)
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def invalid_token():
    response = api_abort(401, error='invalid_token', error_description='Either the token was expired or invalid')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def invalid_id():
    response = api_abort(401, error='invalid id', error_description="this post doesn't exist.")
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def login_required():
    res = api_abort(401, error='Login Required', error_description='You need to login first.')
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def arg_required(info):
    res = api_abort(401, error='A required argument was absent', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res
