from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'