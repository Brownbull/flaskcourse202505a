from flask import Flask, request

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
# http://127.0.0.1:5000/dynamic/asdasd

@app.route("/query")
def query_route():
  name = request.args.get("name")
  world = request.args.get("world")
  return f"<h1>Hello, {name} and {world}!</h1>"
# http://127.0.0.1:5000/query?name=asd%20asd&world=123