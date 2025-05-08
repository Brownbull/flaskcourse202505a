from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return "<h1>Hello, World!</h1>"

@app.route("/home")
def home():
  return "<h1>Welcome to the Home Page!</h1>"

@app.route("/json")
def json_response():
  return {
    "message": ["Hello", "JSON!"],
    "status": "success"
  }

