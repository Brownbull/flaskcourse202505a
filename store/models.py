from .extensions import db
from flask_login import UserMixin

class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
