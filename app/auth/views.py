import datetime
import os
from . import auth
from flask import request, jsonify, g, session, send_file, current_app
from ..model import User, Role
from .. import db
from werkzeug.utils import secure_filename
from .errors import page_not_found, arg_required
from .authentication import user_verify_password
from .errors import (unauthorized, duplicate_phone,
                     unsupportedMediaType, invalid_token,
                     token_missing, wrong_password, file_not_found)


@auth.route('/login', methods=["POST"])
def login():
    grant_type = request.form.get('grant_type') if request.form.get('grant_type') is not None else request.args.get(
        'grant_type')
    if grant_type is None:
        arg_required(info='argument required:grant_type,whose value should be "password"')
    phone = request.form.get('phone')
    password = request.form.get('password')
    if phone is None or password is None:
        phone = request.args.get('phone')
        password = request.args.get('password')
    rescode = user_verify_password(phone, password)
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


# def get_routes(bp_names):
#     routes = [rule for rule in current_app.url_map.iter_rules() if rule.endpoint.startswith(bp_names)]
#     li = []
#     for route in routes:
#         ro = Route(route.endpoint, route.methods)
#         li.append(ro.toJson())
#     print(li)
#     return li


# @auth.route('/', methods=['GET', 'POST'])
# def index():
#     return jsonify(get_routes(request.blueprint))
#     # return get_routes(request.blueprint)


@auth.route('/user', methods=['POST', 'GET'])
def get_current_user():
    token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
    if token is not None:
        boolean, user = User.test_verify_code(token)
        if boolean:
            res = user.to_json()
            return res
        else:
            res = invalid_token()
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


def isFileExtensionAllowed(filename: str) -> bool:
    if filename.rsplit('.')[-1].lower() in current_app.config['ALLOWED_EXTENSION']:
        return True
    return False


def isAllowedSize(file) -> bool:
    if file.content_length > current_app.config['MAX_CONTENT_LENGTH']:
        return False
    return True


@auth.route('/register', methods=['POST'])
def register():
    phone = request.form.get('phone')
    name = request.form.get('name')
    password_hash = request.form.get('password')

    if phone is None or name is None or password_hash is None:
        phone = request.args.get('phone')
        name = request.args.get('name')
        password_hash = request.args.get('password')

    if 'avatar' in request.files:
        avatar = request.files['avatar']
        if isFileExtensionAllowed(avatar.filename) and isAllowedSize(avatar):
            filelist = os.listdir(current_app.config['UPLOAD_FOLDER'])
            num = filelist.count(avatar.filename)
            if num > 0:
                avatar.filename = avatar.filename.split('.')[0] + '({0})'.format(num) + avatar.filename.rsplit('.')[-1]
            avatar_filename = secure_filename(avatar.filename)
            avatar.save(avatar_filename)
        else:
            error_msg = 'Allowed Extensions are showing as bellow:' + str(current_app.config['ALLOWED_EXTENSION'])
            res = unsupportedMediaType(error_msg)
            return res
    else:
        # 使用默认头像
        avatar_filename = 'Default Avatar'
    print(phone, password_hash, name)
    is_duplicate, error_msg = User.is_duplicated(phone, name)
    if is_duplicate:
        res = duplicate_phone(error_msg)
        return res
    else:
        user = User(phone=phone, name=name, password_hash=password_hash, is_authenticated=True, avatar=avatar_filename)
        # try:
        Role.insert_roles()
        db.session.add(user)
        db.session.commit()
        token = user.to_json()
        return token


@auth.route('/modify_profile', methods=["POST"])
def modify_profile():
    token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
    if token is None:
        response = token_missing()
        return response
    phone = request.form.get('phone')
    name = request.form.get('name')
    if phone is None or name is None or token is None:
        phone = request.args.get('phone')
        name = request.args.get('name')
        boolean, user = User.test_verify_code(token)
        if not boolean:
            response = invalid_token()
            return response
        user.phone = phone
        user.name = name
        db.session.add(user)
        db.session.commit()
        return user.to_json()


@auth.route('/verify_password', methods=['POST'])
def verify_password():
    token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
    if token is None:
        response = token_missing()
        return response
    password = request.form.get('password') if request.form.get('password') is not None else request.args.get(
        'password')
    boolean, user = User.test_verify_code(token)
    if boolean:
        print(user.password_hash)
        print(password)
        if password == user.password_hash:
            return jsonify({
                'status': 1,
                'success': True
            })
        else:
            return jsonify({
                'status': 0,
                'success': False
            })
    else:
        res = invalid_token()
        return res


@auth.route('/change_password', methods=['POST'])
def change_password():
    token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
    if token:
        old_pwd = request.form.get('old_password') if request.form.get(
            'old_password') is not None else request.args.get('old_password')
        new_pwd = request.form.get('new_password') if request.form.get(
            'new_password') is not None else request.args.get('new_password')
        boolean, user = User.test_verify_code(token)
        if boolean:
            if user.password_hash == old_pwd:
                user.password_hash = new_pwd
                db.session.add(user)
                db.session.commit()
                res = user.to_json()
                return res
            else:
                res = wrong_password()
                return res
        else:
            res = invalid_token()
            return res
    else:
        res = arg_required('token required')
        return res


@auth.route('/logout')
def logout():
    return ({
        'state': 200,
        'info': 'logout success'
    })


@auth.route('/avatar', methods=['GET', 'POST'])
def getAvatar():
    """
    :info: 使用查询字符串方式获取头像文件
    :return: 返回Response类型数据，即相应的图片
    """
    file_path = request.args.get('file_path') if request.args.get('file_path') else request.form.get('file_path')
    if not file_path:
        res = arg_required(info="'file_path' needed.")
        return res
    if file_path == 'Default':
        filepath = current_app.config['DEFAULT_AVATAR_PATH']
    else:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
    try:
        return send_file(filepath, mimetype='image/gif')
    except FileNotFoundError as e:
        print(e)
        res = file_not_found(
            info='Requested file not found in Server.Check the file_path again or contact the developer')
        return res


@auth.route('/avatar/filename=<filename>', methods=['GET'])
def getAvatar_(filename):
    if not filename:
        res = arg_required(info="'file_path' needed.")
        return res
    if filename == 'Default':
        filepath = current_app.config['DEFAULT_AVATAR_PATH']
    else:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    try:
        return send_file(filepath, mimetype='image/gif')
    except FileNotFoundError as e:
        print(e)
        res = file_not_found(
            info='Requested file not found in Server.Check the file_path again or contact the developer')
        return res
