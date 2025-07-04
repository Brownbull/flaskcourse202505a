from sqlalchemy import create_engine

engine = create_engine('sqlite:///instance/migrations.db')

with engine.connect() as conn:
    pass