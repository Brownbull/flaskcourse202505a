from flask import Flask

from .commands import create_tables
from .extensions import db, migrate
from .routes import main

def create_app():
  app = Flask(__name__)

  app.config.from_prefixed_env()

  db.init_app(app)
  migrate.init_app(app, db)

  app.register_blueprint(main)
  
  app.cli.add_command(create_tables)

  return app