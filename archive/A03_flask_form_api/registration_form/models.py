from datetime import datetime
from werkzeug.security import generate_password_hash

from .extensions import db

member_topic_table = db.Table(
    'member_topic',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True)
)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    first_learn_date = db.Column(db.Date, nullable=True)
    fav_language = db.Column(db.ForeignKey('language.id'), nullable=True)
    about = db.Column(db.Text)
    learn_new_interest = db.Column(db.Boolean)

    interest_in_topics = db.relationship(
        'Topic',
        secondary = member_topic_table,
        lazy = True,
        backref=db.backref('topic', lazy=True)
    )

    @property
    def password(self):
        raise AttributeError('Cannot read password attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_json(self):
        """Convert the Member instance to a JSON serializable dictionary."""
        interest_in_topics_json = [{'id': topic.id, 'name': topic.name} for topic in self.interest_in_topics]

        language_json = {}
        fav_language = Language.query.get(self.fav_language)
        if self.fav_language:
            language_json = {
                'id': fav_language.id,
                'name': fav_language.name
            }

        member_json = {
            'id': self.id,
            'email': self.email,
            'location': self.location,
            'first_learn_date': datetime.strftime(self.first_learn_date, '%Y-%m-%d') if self.first_learn_date else '', 
            # 'first_learn_date': self.first_learn_date.isoformat() if self.first_learn_date else None,
            'fav_language': language_json,
            'about': self.about,
            'learn_new_interest': self.learn_new_interest,
            'interest_in_topics': interest_in_topics_json
        }

        return member_json



class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)