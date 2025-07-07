from .extensions import db
from flask_login import UserMixin

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)
    join_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    following = db.relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
    )

    followed_by = db.relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.followed_id == id),
        secondaryjoin = (followers.c.follower_id == id),
        backref = db.backref('followees', lazy='dynamic'),
        lazy = 'dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.id} by {self.user.username}>'
    