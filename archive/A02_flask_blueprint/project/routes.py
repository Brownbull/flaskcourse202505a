from flask import Blueprint
from .models import MyModel
from .extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return "<h1>Welcome to the Flask App! in blueprint</h1>"