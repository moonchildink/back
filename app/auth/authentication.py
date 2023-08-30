from flask_httpauth import HTTPBasicAuth
from flask import g
from ..model import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(phone, password):
    """
    修改逻辑，使其支持通过密钥登录
    :param phone:
    :param password:
    :return:
    """
    if phone and password:
        user = User.query.filter_by(phone=phone).first()
        if phone == user.phone:
            g.current_user = user
            return user.verify_password(password)
        else:
            return False
    else:
        return False
