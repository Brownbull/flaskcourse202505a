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

  def __repr__(self):
    return f"<User {self.name}>"



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
  new_user = User(
    name="Gabe", 
    date_joined=datetime.now(), 
    email="carcamo.gabriel@gmail.com")
  db.session.add(new_user)
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