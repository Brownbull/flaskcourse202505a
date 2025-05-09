from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "Hello, World!"
    
    return app