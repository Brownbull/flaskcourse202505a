from flask import Flask, render_template
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    main = Blueprint('main', __name__)
    app.register_blueprint(main)
    
    @app.route('/')
    def index():
        return "Hello, World!"
    
    return app