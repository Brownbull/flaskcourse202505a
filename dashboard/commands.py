import click
from random import randint, choice

from faker import Faker
from flask.cli import with_appcontext
from sqlalchemy.sql import func
from sqlalchemy import text

from .extensions import db
from .models import Customer, Order, Product

fake = Faker()

@click.command(name = 'create_tables')
@with_appcontext
def create_tables():
    """Create the database tables."""
    db.create_all()
    click.echo('Database tables created successfully.')

@click.command(name = 'create_products')
@with_appcontext
def create_products():
    """Create sample products."""
    products = [
        Product(name='Product 1', price=10, monthly_goal = 1000),
        Product(name='Product 2', price=25, monthly_goal = 4000),
        Product(name='Product 3', price=90, monthly_goal = 3000)
    ]
    db.session.bulk_save_objects(products)
    db.session.commit()
    click.echo('Sample products created successfully.')

@click.command(name = 'create_orders')
@with_appcontext
def create_orders():
    products = Product.query.all()
    for _ in range(100):
        customer = Customer(
            name=fake.name(),
        )
        db.session.add(customer)
        db.session.flush()

        quantity = randint(1, 7)
        product = choice(products)
        date = fake.date_between(start_date='-600d', end_date='now')
        order = Order(
            customer_id = customer.id,
            product_id = product.id,
            quantity = quantity,
            order_date = date
        )
        db.session.add(order)
        
    # Commit all orders at once
    db.session.commit()
    click.echo('Sample orders created successfully.')

@click.command(name = 'test_query')
@with_appcontext
def test_query():
    revenue_per_product = db.session.query(\
        Product.name, \
        func.sum(Order.quantity * Product.price))\
        .join(Order)\
        .group_by(Product.name)\
        .all()

    monthly_earnings = db.session.query(\
        func.extract('year', Order.order_date), \
        func.extract('month', Order.order_date), \
        func.sum(Order.quantity * Product.price),\
        func.count())\
        .join(Product)\
        .group_by(\
            func.extract('year', Order.order_date),
            func.extract('month', Order.order_date))\
        .all()
    print(revenue_per_product)

@click.command(name = 'test_SQL')
@with_appcontext
def test_SQL():
    qry_out = db.session.execute(text('''
        SELECT 
            p.name AS product_name,
            SUM(o.quantity * p.price) AS total_revenue
        FROM orders o
        JOIN products p 
        ON o.product_id = p.id
        GROUP BY p.name
        ORDER BY p.name
    ''')).fetchall()

    monthly_earnings = db.session.execute(text('''
        SELECT 
            strftime('%Y', o.order_date) AS year,
            strftime('%m', o.order_date) AS month,
            SUM(o.quantity * p.price) AS total_revenue,
            COUNT(*) AS order_count
        FROM orders o
        JOIN products p 
        ON o.product_id = p.id
        GROUP BY year, month
        ORDER BY year, month
    ''')).fetchall()
    print(qry_out)
    click.echo('Direct query executed successfully.')