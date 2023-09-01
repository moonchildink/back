import datetime
from . import auth
from flask import request, jsonify, g, session
from ..model import User, Role
from .. import db
from .errors import page_not_found, arg_required
from .authentication import verify_password
from .errors import unauthorized, duplicate_phone, server_interval_error, invalid_token, token_missing


@auth.route('/login', methods=["POST"])
def login():
    grant_type = request.form.get('grant_type')
    if grant_type is None or grant_type.lower() != 'password':
        arg_required()
    phone = request.form.get('phone')
    password = request.form.get('password')
    if phone is None or password is None:
        phone = request.args.get('phone')
        password = request.args.get('password')
    rescode = verify_password(phone, password)
    if rescode == 1:
        # 获取当前用户信息，返回格式化后的json字符串
        user = User.query.filter_by(phone=phone).first()
        user.generate_verify_code()
        user.last_login = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        session['current_user_id'] = user.id
        res = user.to_json()
        return res
    elif rescode == 0:
        res = unauthorized('wrong password', 401)
        return res
    elif rescode == -1:
        res = unauthorized('phone num has not been registered', 402)


@auth.route('/', methods=['POST'])
def index():
    """
    ！注意！：当前路由仅可以在登陆后访问，需要携带当前用户的jwt
    :return: 当前蓝图下所有可访问的资源
    """
    return jsonify({
        'api_version': '1.0',
        'api_base_url': 'http://127.0.0.1:5000/auth',
        'current_user_url': 'http://127.0.0.1:5000/auth/user/<int:id>'
    })


@auth.route('/user', methods=['POST', 'GET'])
def get_current_user():
    token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
    if token is not None:
        user = User.test_verify_code(token)
        res = user.to_json()
        return res
    else:
        res = arg_required("argument 'token' is required")
        return res


@auth.route('/user/<int:id>', methods=['GET', 'POST'])
def get_current_user_via_id(id):
    try:
        user = User.query.get(id)
        res = user.to_json()
        return res
    except Exception as e:
        page_not_found(str(e))


@auth.route('/register', methods=['POST'])
def register():
    phone = request.form.get('phone')
    name = request.form.get('name')
    password_hash = request.form.get('password')
    is_authenticated = True
    if phone is None or name is None or password_hash is None:
        phone = request.args.get('phone')
        name = request.args.get('name')
        password_hash = request.args.get('password')
    print(phone, password_hash, name)
    is_duplicate, error_msg = User.is_duplicated(phone, name)
    if is_duplicate:
        res = duplicate_phone(error_msg)
        return res
    else:
        user = User(phone=phone, name=name, password_hash=password_hash, is_authenticated=True)
        # try:
        Role.insert_roles()
        db.session.add(user)
        db.session.commit()
        token = user.to_json()
        return token


@auth.route('modify_profile', methods=["POST"])
def modify_profile():
    token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
    if token is None:
        response = token_missing()
        return response
    phone = request.form.get('phone')
    password = request.form.get('password')
    name = request.form.get('name')
    if phone is None or password is None or name is None or token is None:
        phone = request.args.get('phone')
        password = request.args.get('password')
        name = request.args.get('name')
    # token译码
    try:
        user = User.test_verify_code(token)
        if user is None:
            response = token_missing()
            return response
        user.phone = phone
        user.name = name
        user.phone = user.phone
        user.password_hash = password
        db.session.add(user)
        db.session.commit()
        return user.to_json()
    except Exception as e:
        res = invalid_token()
        return res


@auth.route('logout')
def logout():
    token = request.form.get('token')
    user_id = User.test_verify_code(token)
    # 销毁token

    return ({
        'state': 200,
        'info': 'logout success'
    })
