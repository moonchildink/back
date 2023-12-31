from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


# 无权访问状态码403
def forbidden(message):
    res = jsonify({
        'error': 'forbidden',
        'msg': message
    })
    res.status_code = 403
    return res


# page not found
def page_not_found(message):
    res = jsonify({
        'error': 'page not found',
        'msg': message
    })
    res.status_code = 404
    return res


# 服务器内部错误
def server_interval_error(message):
    res = jsonify({
        'error': 'server interval error',
        'msg': message
    })
    res.status_code = 500
    return res


def unauthorized(message, status_code):
    res = jsonify({
        'error': 'unauthorized',
        'msg': message
    })
    res.status_code = status_code
    return res


def duplicate_phone(message):
    res = jsonify({
        'error': 'duplicated phone number',
        'msg': message
    })
    res.status_code = 401
    return res


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


def login_required():
    res = api_abort(401, error='Login Required', error_description='You need to login first.')
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def wrong_password():
    res = api_abort(401, error='Wrong Password', error_description='Your password is wrong')
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def arg_required(info=None):
    res = api_abort(401, error='A required argument was absent', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def unsupportedMediaType(info=None):
    res = api_abort(415, error='Unsupported Media Type', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def requestEntityTooLarge(info=None):
    res = api_abort(413, error='Request Entity too Large', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def file_not_found(info=None):
    res = api_abort(404, error='Source not found', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res
