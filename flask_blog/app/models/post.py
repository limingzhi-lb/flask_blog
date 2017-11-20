from app.extensions import db
from datetime import datetime


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    rrid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
