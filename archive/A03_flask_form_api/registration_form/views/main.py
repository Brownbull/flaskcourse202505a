from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for

from registration_form.models import Language, Topic, Member
from registration_form.extensions import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'], defaults = {'member_id': None})
@main.route('/<int:member_id>', methods=['GET', 'POST'])
def index(member_id):
    member = None
    if member_id:
        member = Member.query.get_or_404(member_id)

    errors = {}
    
    if request.method == 'POST':
        # Get input
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        first_learn_date = request.form['first_learn_date']
        fav_language = request.form['fav_language']
        about = request.form['about']
        learn_new_interest = request.form['learn_new_interest']
        interest_in_topics = request.form.getlist('interest_in_topics')

        # Validate input
        if not email:
            errors['email'] = 'Email is required.'
        if not password and not member_id:  # Only require password if creating a new member
            errors['password'] = 'Password is required.'
        if not location:
            errors['location'] = 'Location is required.'
        if not first_learn_date:
            errors['first_learn_date'] = 'First learn date is required.'
        if not about:
            errors['about'] = 'About section is required.'
        if not interest_in_topics:
            errors['interest_in_topics'] = 'At least one topic of interest is required.'
        if not errors:
            print('No errors')

            if member:
                # UDPATE existing member
                member.email = email
                if password:
                    member.password = password
                member.location = location
                member.first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d') if first_learn_date else None
                member.fav_language = fav_language
                member.about = about
                member.learn_new_interest = True if learn_new_interest == "Yes" else False
                member.interest_in_topics[:] = []  # Clear existing topics
            else:
                # CREATE new member
                member = Member(
                    email = email,
                    password = password,
                    location = location,
                    first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d') if first_learn_date else None,
                    fav_language = fav_language,
                    about = about,
                    learn_new_interest = True if learn_new_interest == "Yes" else False,
                )

                db.session.add(member)

            for topic_id in interest_in_topics:
                topic = Topic.query.get(topic_id)
                if topic:
                    member.interest_in_topics.append(topic)

            db.session.commit()
            print('Member added to database:', member)

            return redirect(url_for('main.index', member_id=member.id))
    
    languages = Language.query.all()
    topics = Topic.query.all()

    context = {
        'member_id': member_id,
        'languages': languages,
        'topics': topics,
        'member': member,
        'errors': errors
    }

    return render_template('form.html', **context)