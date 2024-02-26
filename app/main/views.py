from . import main
from flask import request, current_app
import os
from .. import db
from ..I3D import Predictor
from ..model import Video, User
from .error import invalid_token, unsupportedMediaType, token_missing


# predicator = Predictor()


def saveFile(avatar):
    filelist = os.listdir(current_app.config['UPLOAD_FOLDER'])
    num = filelist.count(avatar.filename)
    if num > 0:
        avatar.filename = avatar.filename.split('.')[0] + '({0})'.format(
            num) + '.' + avatar.filename.rsplit('.')[-1]
    else:
        avatar.filename = avatar.filename
    avatar.save(os.path.join(current_app.config['UPLOAD_FOLDER'], avatar.filename))
    return avatar.filename


def isFileExtensionAllowed(filename: str) -> bool:
    return ('.' in filename and
            filename.rsplit('.')[-1].lower() in current_app.config['ALLOWED_EXTENSION'])


@main.route('/', methods=['GET'])
def index():
    return 'hello'

@main.route('/video_upload', methods=['POST'])
def video_upload():
    # 接收前端传输的视频并保存_
    # 预测结果
    if 'video' in request.files:
        token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
        if token is None or token == '':
            res = invalid_token()
            return res
        else:
            boolean, user = User.test_verify_code(token)
            if boolean:
                sign_video = request.files['video']
                if isFileExtensionAllowed(sign_video.filename):
                    video_save_path = saveFile(sign_video)
                    label = get_predication(video_save_path)
                    video = Video(video_path=video_save_path, video_predication=label, uploader=User)
                    db.session.add(video)
                    db.session.commit()
                    res = video.to_json()
                    return res
                else:
                    err_msg = 'Current File Extension is NOT ALLOWED'
                    res = unsupportedMediaType(err_msg)
                    return res
    else:
        res = token_missing()
        return res


def get_predication(video_path):
    # label = predicator.predicate(video_path)
    # return label
    pass
