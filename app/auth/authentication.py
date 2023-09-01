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
    # if phone and password:
    #     user = User.query.filter_by(phone=phone).first()
    #     if user and phone == user.phone:
    #         g.current_user = user
    #         return user.verify_password(password)
    #     else:
    #         return False
    # else:
    #     return False

    if phone and password:
        user = User.query.filter_by(phone=phone).first()
        if user:
            if user.password_hash == password:
                return 1
            else:
                return 0        # 0 表示密码错误
        else:
            return -1           # -1 表示当前手机号码未注册
