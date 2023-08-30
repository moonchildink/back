from flask import Blueprint
from flask_cors import CORS

post = Blueprint('post',__name__)

CORS(post)

from . import  views