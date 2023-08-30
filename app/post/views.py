import datetime
from ..search import ProcessInput
from .. import db
from json import dumps
from ..model import User, Post, Role, Follow, Permission
from . import post
from flask import request, jsonify
from .errors import login_required, arg_required, invalid_id, invalid_token


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
            user = User.test_verify_code(token)
            if user.can(Permission.WRITE):
                post = Post(title=title, content=content, timestamp=datetime.datetime.utcnow(),
                            author=user, reads=0, last_edit_time=datetime.datetime.utcnow())
                db.session.add(post)
                db.session.commit()
                res = post.to_json()
                return res
            else:
                res = invalid_token()
                return res


@post.route('/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    return post.to_json()


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
        user = User.test_verify_code(token)
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


@post.route('/', methods=['GET'])
def index():
    return jsonify({
        'api_version': '1.0',
        'api_base_url': 'http://127.0.0.1/post',
        'add_new_post': '/new',
        'delete_post': '/delete',
        'search_post': '/search',
        "user's post": '/my_post/',
        'query_post': '?<id>'
    })