from app.extensions import db, login_manage
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.email import send_mail
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    icon = db.Column(db.String(64), default='default.jpg')
    confirmed = db.Column(db.Boolean, default=False)
    posts = db.relationship('Posts', backref='user', lazy='dynamic')

    def generate_activate_token(self, expiers_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'id': 'lmz'})
        return s.dumps({'id': self.id})

    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        return '%s账户已经激活' % data.get('id')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manage.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))
