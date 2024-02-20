from flask_login import UserMixin, AnonymousUserMixin
from . import db
import datetime
import jwt
from flask import current_app, jsonify
from . import login_manager


class Permission:
    """
    权限说明：
        1. 识别手语：RECOGNITION 1
        2. 关注其他用户：FOLLOW 2
        3. 评论：COMMENT 4
        4. 发帖子：WRITE 8
        5. 管理帖子和评论：MODERATE 16
        6. 管理员：ADMIN 32
    """
    RECOGNITION = 1
    FOLLOW = 2
    COMMENT = 4
    WRITE = 8
    MODERATE = 16
    ADMIN = 32


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    permission = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    name = db.Column(db.String(16), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.RECOGNITION, Permission.FOLLOW, Permission.COMMENT,
                     Permission.WRITE],
            'Moderator': [Permission.RECOGNITION, Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.RECOGNITION, Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.reset_permissions()
                for perm in roles[r]:
                    role.add_permissions(perm)
                role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permissions(self, perm):
        self.permission += perm

    def remove_permission(self, perm):
        self.permission -= perm

    def reset_permissions(self):
        self.permission = 0

    def has_permission(self, permission):
        return self.permission & permission == permission

    def __repr__(self):
        return '<Role %r>' % self.name



class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())



class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    video_path = db.Column(db.String(64), nullable=False, unique=True)
    video_predication = db.Column(db.String(10), nullable=False, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return jsonify({
            'uploader': {
                'id': self.uploader.id,
                'name': self.uploader.name,
                'phone': self.uploader.phone,
                'avatar_path': self.uploader.avatar_path
            },
            'timestamp': self.timestamp,
            'predication': self.video_predication
        })

    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    reads = db.Column(db.Integer, default=0)
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return jsonify({
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'time': self.timestamp,
            'timestamp': self.timestamp.timestamp(),
            'last_edit_time': self.last_edit_time,
            'reads': self.reads,
            'author': {
                'id': self.author.id,
                'name': self.author.name,
                'phone': self.author.phone,
                'avatar_path': self.author.avatar_path
            }
        })

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(32), unique=False, nullable=False)
    phone = db.Column(db.String(16), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    gender = db.Column(db.Integer, default=1)  # 1代表男性，0代表女性
    is_authenticated = db.Column(db.Boolean, unique=False)
    register_time = db.Column(db.DATETIME(), default=datetime.datetime.utcnow())
    last_login = db.Column(db.DATETIME(), default=datetime.datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    videos = db.relationship('Video', backref='uploader', lazy='dynamic')
    avatar_path = db.Column(db.String(128), unique=False, nullable=False)  # 如果使用系统默认头像那么该字段为空
    followed = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic', cascade='all,delete-orphan')
    follower = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic', cascade='all,delete-orphan')

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        Role.insert_roles()
        if self.role is None:
            if self.phone in current_app.config['ADMIN_PHONES']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
                self.role_id = self.role.id

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.role is not None and self.role.has_permission(Permission.ADMIN)

    def verify_password(self, password):
        if password == self.password_hash:
            return True
        else:
            return False

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(self, user)
            db.session.add(follow)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.follower.filter_by(follower_id=user.id).first() is not None

    def generate_verify_code(self):
        """
        使用JWT作为
        :return: json web token
        """
        payload = {
            'user_id': self.id,
            'username': self.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14)
        }
        jws_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jws_token

    @staticmethod
    def is_duplicated(phone, name):
        res = User.query.filter_by(phone=phone).first()
        if res is None:
            res = User.query.filter_by(name=name).first()
            if res is None:
                return False, 'success'
            return True, 'this name has been existed in database'
        return True, 'this phone has been existed in database'

    @staticmethod
    def test_verify_code(payload):
        secret_key = current_app.config['SECRET_KEY']
        try:
            token = jwt.decode(payload, secret_key, algorithms='HS256')
        # except Exception as e:
        #     return str(e)
        except jwt.ExpiredSignatureError:
            return False, 401
        except jwt.DecodeError:
            return False, 402
        return True, User.query.get(token['user_id'])

    def getJson(self):
        return jsonify({
            'name': self.name,
            'phone': self.phone,
            'password': self.password_hash
        })

    def to_json(self):
        return jsonify({
            'user_id': self.id,
            'name': self.name,
            'phone': self.phone,
            'gender': 'male' if self.gender == 1 else 'female',
            'password': self.password_hash,
            'last_login': self.last_login,
            'is_authenticated': self.is_authenticated,
            'register_time': self.register_time,
            'role_id': self.role_id,
            'token': self.generate_verify_code(),
            'last_login_timestamp': self.last_login.timestamp(),
            'register_time_stamp': self.register_time.timestamp(),
            'avatar_path': self.avatar_path
        })


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user
