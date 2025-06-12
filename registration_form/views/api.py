from datetime import datetime
from flask import Blueprint, jsonify, request

from registration_form import db

from registration_form.models import Member, Topic

api = Blueprint('api', __name__)

@api.route('/member', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify({'members': [member.to_json() for member in members]}), 200

@api.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get_or_404(member_id)
    return jsonify({'member': member.to_json()}), 200

@api.route('/member', methods=['POST'])
def create_member():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    member = Member(
        email = data.get('email'),
        password = data.get('password'),
        location = data.get('location'),
        first_learn_date = datetime.strptime(
            data.get('first_learn_date'), 
            '%Y-%m-%d'),

        fav_language = data['fav_language'].get('id'),
        about = data.get('about'),
        learn_new_interest = data.get('learn_new_interest'),
    )

    topics = data.get('interest_in_topics', [])
    for member_topic in topics:
        topic = Topic.query.get(member_topic['id'])
        member.interest_in_topics.append(topic)

    try:
        db.session.add(member)
        db.session.commit()
        return jsonify({'member': member.to_json()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


    