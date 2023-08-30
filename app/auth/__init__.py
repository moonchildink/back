from flask import Blueprint
from flask_cors import CORS

auth = Blueprint('auth',__name__)

# 添加跨域支持
CORS(auth)


from . import views,authentication