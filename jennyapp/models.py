from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    phone_number_1 = db.Column(db.String(20), nullable=True)
    phone_number_2 = db.Column(db.String(20), nullable=True)
    address_1 = db.Column(db.String(200), nullable=True)
    address_2 = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    notifications = db.Column(db.Boolean, nullable=True)
    join_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # ME
    medical_history = db.Column(db.String(200), nullable=True)
    current_medications = db.Column(db.String(200), nullable=True)
    allergies = db.Column(db.String(200), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_number = db.Column(db.String(20), nullable=True)
    emergency_contact_relationship = db.Column(db.String(100), nullable=True)

    # @property
    # def date_of_birth(self):
    #     raise AttributeError('date_of_birth is not a readable attribute')
    # @date_of_birth.setter
    # def date_of_birth(self, date_of_birth):
    #     self.date_of_birth_sql = datetime.strptime(date_of_birth, '%Y-%m-%d') if date_of_birth else None
        
    # @date_of_birth.getter
    # def date_of_birth(self):
    #     return self.date_of_birth_sql.strftime('%Y-%m-%d') if self.date_of_birth_sql else ''
