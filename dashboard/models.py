from datetime import datetime
from sqlalchemy import func
from .extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    monthly_goal = db.Column(db.Integer)

    def revenue_per_month(self):
        first_day_of_month = datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        return db.session.query(
            db.func.sum(Order.quantity * self.price)
        ).filter(Order.product_id == self.id,
            Order.order_date > first_day_of_month
        ).scalar() or 0
    
class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)

    # customer = db.relationship('Customers', backref=db.backref('orders', lazy=True))
    # product = db.relationship('Product', backref=db.backref('orders', lazy=True))

