"""
@author: moonhchild
@date: 2023/6/28
"""
import os

JSON_AS_ASCII = True
MAX_CONTENT_LENGTH = 5 * 1000 * 1000  # 限制用户上传文件的大小
UPLOAD_FOLDER = r"D:\code\population_back\upload_files"
ALLOWED_EXTENSION = 'txt'
SECRET_KEY = 'vz\x92\xf1\xa5\xfc7\xef\xe1\xa9\xa6\xd0\xcd\xad\xd0\x81\x14/\x07F\xe1\x0f\x90\x8c'


class Config:
    SECERT_KEY = os.environ.get(
        "SECERT_KEY") or 'vz\x92\xf1\xa5\xfc7\xef\xe1\xa9\xa6\xd0\xcd\xad\xd0\x81\x14/\x07F\xe1\x0f\x90\x8c'
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = '465'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'moonchild.hh@foxmail.com'
    MAIL_PASSWORD = "ecduqculoooddfee"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DeploymentConfig(Config):
    DEBUG = False
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    USERNAME = 'user'
    PASSWORD = 'eA2NJw3CWJie8nnT'
    SECRET_KEY = 'Mwoo1764'
    VIDEO_DIR = '../../all_video/'
    UPLOAD_FOLDER = r'/data/UpLoadFiles'
    DEFAULT_AVATAR_PATH = '../../UpLoadFiles/Default.jpg'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSION = ['jpg', 'jpeg', '.xbm', '.tif', '.mp4', '.jfif', ',webp', 'png', 'bmp']
    DATABASE = 'database'
    ADMIN_PHONES = ['18856364286']
    SQLALCHEMY_DATABASE_URI = \
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


class WSL_Config(Config):
    DEBUG = False
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    USERNAME = 'user'
    PASSWORD = 'yZDWwtacMzsST24B'
    SECRET_KEY = 'Mwoo1764'
    UPLOAD_FOLDER = r'/data/UpLoadFiles'
    DEFAULT_AVATAR_PATH = '../../UpLoadFiles/Default.jpg'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSION = ['jpg', 'jpeg', '.xbm', '.tif', '.mp4', '.jfif', ',webp', 'png', 'bmp']
    DATABASE = 'database'
    ADMIN_PHONES = ['18856364286']
    SQLALCHEMY_DATABASE_URI = \
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


class DevelopmentConfig(Config):
    SECRET_KEY = 'Mwoo1764'
    DEBUG = True
    HOSTNAME = '127.0.0.1'  # 设置数据库的IP地址
    SESSION_PERMANENT = False
    UPLOAD_FOLDER = r'D:\code\Python\flaskProject\UpLoadFiles'
    DEFAULT_AVATAR_PATH = r'D:\code\Python\flaskProject\UpLoadFiles\DefaultAvatar.jpg'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSION = ['jpg', 'jpeg', '.xbm', '.mp4', '.tif', '.jfif', ',webp', 'png', 'bmp']
    SESSION_TYPE = 'filesystem'
    PORT = '3306'
    USERNAME = 'root'
    VIDEO_DIR = '../../all_video/'
    PASSWORD = "112358"
    DATABASE = "new_schema"
    SQLALCHEMY_DATABASE_URI = \
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    ADMIN_PHONES = ['carise0102@gmail.com', '2923636177@qq.com']


config = {
    'development': DevelopmentConfig,
    'deploy': DeploymentConfig,
    'wsl': WSL_Config,
    'default': DevelopmentConfig
}
