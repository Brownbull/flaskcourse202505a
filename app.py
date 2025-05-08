from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return "<h1>Hello, World!</h1>"

@app.route("/home", methods=["POST"])
def home():
  return "<h1>Welcome to the Home Page!</h1>"

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