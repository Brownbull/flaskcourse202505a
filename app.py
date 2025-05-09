from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())
  email = db.Column(db.String(120), unique=True, nullable=False)

  orders = db.relationship("Order", back_populates="user")

  def __repr__(self):
    return f"<User {self.name}>"
  
order_product_table = db.Table("order_product_table",
  db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
  db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True))
  
class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  total_price = db.Column(db.Float, nullable=False, default=0.0)

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  user = db.relationship("User", back_populates="orders")

  products = db.relationship("Product", secondary = order_product_table, back_populates="orders")
  def __repr__(self):
    return f"<Order {self.id}>"
  
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=False)

  orders = db.relationship("Order", secondary=order_product_table, back_populates="products")

  def __repr__(self):
    return f"<Product {self.name}>"


@app.route("/")
def index():
  return render_template("index.html", page_name="Index")
# http://127.0.0.1:5000

@app.route("/home", methods=["GET", "POST"])
def home():
  data = [{"key": "value1"}, {"key": "value2"}]
  return render_template("home.html", number = 21, data = data)             

@app.route("/json")
def json_response():
  return {
    "message": ["Hello", "JSON!"],
    "status": "success"
  }

@app.route("/dynamic", defaults={"name": "World"})
@app.route("/dynamic/<name>")
def dynamic_route(name):
  return f"<h1>Hello, {name}!</h1>"
# http://127.0.0.1:5000/dynamic/asdasd

@app.route("/query")
def query_route():
  name = request.args.get("name")
  world = request.args.get("world")
  return f"<h1>Hello, {name} and {world}!</h1>"
# http://127.0.0.1:5000/query?name=asd%20asd&world=123

@app.route("/form", methods=["GET", "POST"])
def form_route():
  if request.method == "POST":
    user_input = request.form["user_input"]
    print(user_input)
    # Process the input as needed
    return redirect(url_for("home"))
  else:
    # Display the form
    pass
  return "<form method='POST'>\
            <input type='text' name='user_input'>\
            <input type='submit'>\
          </form>"
# http://127.0.0.1:5000/form

@app.route("/input_json", methods=["POST"])
def input_json_route():
  data = request.get_json()
  name = data.get("name")
  age = data.get("age")
  return f"<h1>Name: {name}, Age: {age}</h1>"
# http://127.0.0.1:5000/input_json
"""
{
    "name": "Gabe",
    "age": 36
}
"""

def insert_data():
  from datetime import datetime

  # Users Insertion
  new_user_1 = User(
    name="Gabe", 
    date_joined=datetime.now(), 
    email="carcamo.gabriel@gmail.com")
  new_user_2 = User(
    name="Alejo", 
    date_joined=datetime(2023, 10, 1), 
    email="brownbullforest@gmail.com")
  new_user_3 = User(
    name="Clau", 
    date_joined=datetime(2024, 10, 1), 
    email="cldpn@yahoo.com")

  inserted_users = [new_user_1, new_user_2, new_user_3]
  db.session.add_all(inserted_users)

  # Orders Insertion
  new_order_1 = Order(
    user = new_user_1)
  new_order_2 = Order(
    user = new_user_1)
  new_order_3 = Order(
    user = new_user_2)
  
  inserted_orders = [new_order_1, new_order_2, new_order_3]
  db.session.add_all(inserted_orders)
  
  # Commit the changes to the database
  db.session.commit()
  print("Data inserted successfully!")

def update_data_by_id(id):
  user = User.query.filter_by(id=id).first()
  if user:
    user.name = "Gabriel"
    db.session.commit()
    print("Data updated successfully!")
  else:
    print("User not found.")

def delete_data_by_id(id):
  user = User.query.filter_by(id=id).first()
  if user:
    db.session.delete(user)
    db.session.commit()
    print("Data deleted successfully!")
  else:
    print("User not found.")

def query_data():
  users = User.query.all()
  for user in users:
    print(f"User ID: {user.id}, Name: {user.name}, Date Joined: {user.date_joined}, Email: {user.email}")
    for order in user.orders:
      print(f"  Order ID: {order.id}, Product Name: {order.product_name}, Quantity: {order.quantity}, Total Price: {order.total_price}")

def add_product_to_order():
  product_1 = Product(
    name="Laptop", 
    price=1200)
  product_2 = Product(
    name="Mouse", 
    price=24)
  product_3 = Product(
    name="Keyboard", 
    price=110)
  
  inserted_products = [product_1, product_2, product_3]
  db.session.add_all(inserted_products)

  order_1 = Order.query.filter_by(id=1).first()
  order_1.products.append(product_1)
  order_1.products.append(product_2)

  order_2 = Order.query.filter_by(id=2).first()
  order_2.products.append(product_3)

  db.session.commit()
  print("Data inserted successfully!")

def query_order_products():
  orders = Order.query.all()
  for order in orders:
    print(f"Order ID: {order.id}, Total Price: {order.total_price}")
    for product in order.products:
      print(f"  Product ID: {product.id}, Name: {product.name}, Price: {product.price}")

