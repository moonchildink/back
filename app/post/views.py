import datetime
from ..search import ProcessInput
from .. import db
from json import dumps
from ..model import User, Post, Permission
from . import post
from flask import request, jsonify, current_app
from .errors import arg_required, invalid_id, invalid_token, permission_required


def get_routes(bp_names):
    routes = [rule for rule in current_app.url_map.iter_rules() if rule.endpoint.startswith(bp_names)]
    return routes


@post.route('/', methods=['POST'])
def index():
    return jsonify(get_routes(request.blueprint))


@post.route('/new', methods=['POST'])
def new_post():
    if request.method == 'POST':
        token = request.form.get('token') if request.form.get('token') is not None else request.args.get('token')
        title = request.form.get('title') if request.form.get('title') is not None else request.args.get('title')
        content = request.form.get('content') if request.form.get('content') is not None else request.args.get(
            'content')
        if token is None or token == '':
            res = invalid_token()
            return res
        else:
            boolean, user = User.test_verify_code(token)
            if boolean:
                if user.can(Permission.WRITE):
                    post = Post(title=title, content=content, timestamp=datetime.datetime.utcnow(),
                                author=user, reads=0, last_edit_time=datetime.datetime.utcnow())
                    db.session.add(post)
                    db.session.commit()
                    res = post.to_json()
                    return res
                else:
                    res = permission_required()
                    return res
            else:
                res = invalid_token()
                return res


@post.route('/<int:id>', methods=['GET'])
def get_post(id):
    po = Post.query.get(id)
    if po:
        # 阅读数+1
        reads = po.reads
        reads += 1
        po.reads = reads
        db.session.add(po)
        db.session.commit()
        return po.to_json()
    else:
        res = invalid_id()
        return res


@post.route('/id=<int:post_id>', methods=['GET'])
def getPost(post_id):
    po = Post.query.get(post_id)
    if po:
        return po.to_json()
    else:
        res = invalid_id()
        return res


@post.route('/get_post', methods=['POST'])
def get_post_via_post():
    post_id = request.args.get('post_id') if request.args.get('post_id') is not None else request.form.get('post_id')
    post = Post.query.get(post_id)
    return post.to_json()


@post.route('/my_post', methods=['POST', "GET"])
def my_post():
    token = request.args.get('token') if request.args.get('token') is not None else request.form.get('token')
    if token is None:
        res = arg_required('token missed')
        return res
    else:
        boolean, user = User.test_verify_code(token)
        if boolean:
            posts = user.posts
            post_list = []
            for po in posts:
                js = po.to_json().json
                post_list.append(js)
            dick = dict()
            dick['posts'] = post_list
            dick['length'] = len(post_list)
            dick['user_id'] = user.id
            return dumps(dick)


@post.route('/search', methods=['POST'])
def search_post():
    key_word = request.form.get('key_word') if request.form.get('key_word') is not None \
        else request.args.get('key_word')
    titles = db.session.query(Post.title).all()
    titles = [i[0] for i in titles]
    selected = []
    for title in titles:
        if key_word in title or ProcessInput(key_word, title) > 0.5:
            selected.append(str(title))
    posts = db.session.query(Post).filter(Post.title.in_(selected)).all()
    res = []
    for post in posts:
        res.append(post.to_json().json)
    dick = dict()
    dick['res_list'] = res
    dick['length'] = len(res)
    return jsonify(dick)


@post.route('/delete', methods=['POST'])
def delete_post():
    post_id = request.form.get('post_id') if request.form.get('post_id') is not None else request.args.get('post_id')
    post = Post.query.get(post_id)
    if post is not None:
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            'state': True,
            'info': 'Delete Post Successfully'
        })
    else:
        return invalid_id()


@post.route('/<int:id>', methods=['DELETE'])
def delete_post_via_DELETE(id):
    post = Post.query.get(id)
    if post is not None:
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            'success': True,
            'info': "Delete post successfully."
        })
    else:
        res = invalid_id()
        return res
