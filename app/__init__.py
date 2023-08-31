from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from flask_migrate import Migrate
from flask_session import Session

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

mail = Mail()
db = SQLAlchemy()
session = Session()


def creat_app(config_name='default'):
    """
    创建app的工厂函数,在进行初始化时应使用default参数
    :param config_name: config名称
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # 初始化
    login_manager.init_app(app)
    db.init_app(app)

    migrate = Migrate(app, db)
    session.init_app(app)

    # from .model import Role
    # Role.insert_roles()

    from .auth import auth as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/auth')

    from .post import post as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix='/post')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
