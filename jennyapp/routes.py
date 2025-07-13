from flask import Blueprint, render_template, url_for, redirect, request, current_app, abort
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
UPLOAD_FOLDER = 'static/uploads'

from .extensions import db
from .forms import RegisterForm, LoginForm, PatientForm, SessionForm
from .models import User, Patient, Session

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            error = "Email address already exists. Please use a different email."
        else:
            register_user = User(
                email=form.email.data,
                password=form.password.data,
                join_date=datetime.now()
            )
            db.session.add(register_user)
            db.session.commit()
            login_user(register_user, remember=False) 
            return redirect(url_for('main.dashboard'))
        
    context = {
        'form': form,
        'error': error
    }
    return render_template('register.html', **context)

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.verify_password(form.password.data):
            error = 'Invalid username or password'
        else:
            login_user(user, remember=form.remember_me.data) 
            return redirect(url_for('main.dashboard'))

    context = {
        'form': form,
        'error': error,
    }
    return render_template('login.html', **context)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html')

@main.route('/patients')
@login_required
def patients():
    patients = Patient.query.all()
    return render_template('dashboard/patients/pat_index.html', patients = patients)

@main.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    error = None
    form = PatientForm()
    current_date = datetime.now() 

    if form.validate_on_submit():
        new_patient = Patient(
            full_name = form.full_name.data,
            # date_of_birth = datetime.strptime(form.date_of_birth.data, '%Y-%m-%d').date(),
            date_of_birth=form.date_of_birth.data,
            gender = form.gender.data,
            email = form.email.data,
            phone_number_1 = form.phone_number_1.data,
            phone_number_2 = form.phone_number_2.data,
            address_1 = form.address_1.data,
            address_2 = form.address_2.data,
            city = form.city.data,
            region = form.region.data,
            country = form.country.data,
            zip_code = form.zip_code.data,
            notifications = form.notifications.data,
            join_date = current_date,
            # ME
            medical_history = "",
            current_medications = "",
            allergies = "",
            emergency_contact_name = "",
            emergency_contact_number = "",
            emergency_contact_relationship = "",
            )
        
        db.session.add(new_patient)
        db.session.commit()
        
        return redirect(url_for('main.patients'))
    
    context = {
        'form': form,
        'error': error
    }
    return render_template('dashboard/patients/pat_add.html', **context)

@main.route('/', methods=['GET', 'POST'], defaults = {'patient_id': None})
@main.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    edit_patient = None
    error = {}
    form = PatientForm()

    if patient_id:
        edit_patient = Patient.query.get_or_404(patient_id, description=f'Patient with id {patient_id} not found')
        form = PatientForm(obj=edit_patient)
    else:
        form = PatientForm()
        # print(f"date_of_birth: {edit_patient.date_of_birth} {type({edit_patient.date_of_birth})}")

    if request.method == 'POST':
        print(request.form['notifications'])
        edit_patient.full_name = request.form['full_name']
        edit_patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        edit_patient.gender = request.form['gender']
        # edit_patient.email = edit_patient.email
        edit_patient.phone_number_1 = request.form['phone_number_1']
        edit_patient.phone_number_2 = request.form['phone_number_2']
        edit_patient.address_1 = request.form['address_1']
        edit_patient.address_2 = request.form['address_2']
        edit_patient.city = request.form['city']
        edit_patient.region = request.form['region']
        edit_patient.country = request.form['country']
        edit_patient.zip_code = request.form['zip_code']
        edit_patient.notifications = True if request.form['notifications']  == 'y' else False
        edit_patient.medical_history = request.form['medical_history']
        edit_patient.current_medications = request.form['current_medications']
        edit_patient.allergies = request.form['allergies']
        edit_patient.emergency_contact_name = request.form['emergency_contact_name']
        edit_patient.emergency_contact_number = request.form['emergency_contact_number']
        edit_patient.emergency_contact_relationship = request.form['emergency_contact_relationship']
        db.session.commit()
        print("Patient updated")
        return redirect(url_for('main.patients'))

    context = {
        'form': form,
        'error': error,
        'patient_id': patient_id,
        'edit_patient': edit_patient
    }
    
    return render_template('dashboard/patients/pat_edit.html', **context)

@main.route('/delete_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id, description=f'Patient with id {patient_id} not found')
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('main.patients'))

@main.route('/sessions')
@login_required
def sessions():
    return render_template('dashboard/sessions/ses_index.html')


# Edit or add a session
@main.route('/edit_session', methods=['GET', 'POST'])
@main.route('/edit_session/<int:session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id=None):
    error = None
    session_obj = None
    form = SessionForm()
    form.doctor_email.choices = [(u.email, u.email) for u in User.query.all()]
    form.patient_full_name.choices = [(p.full_name, p.full_name) for p in Patient.query.all()]

    # If editing, load session
    if session_id:
        session_obj = Session.query.get_or_404(session_id, description=f'Session with id {session_id} not found')
        form = SessionForm(obj=session_obj)

    if request.method == 'POST':
        if form.validate_on_submit():
            # If editing, update; else, create new
            if session_obj:
                session_obj.doctor_email = form.doctor_email.data
                session_obj.patient_full_name = form.patient_full_name.data
                session_obj.session_date = form.session_date.data
                session_obj.session_time = form.session_time.data
                session_obj.consent = form.consent.data
                session_obj.reason_for_visit = form.reason_for_visit.data
                session_obj.medications = form.medications.data
                session_obj.payment_method = form.payment_method.data
                session_obj.total_amount = form.total_amount.data
                session_obj.payment_status = form.payment_status.data
            else:
                # Find patient by name (or create new if not found)
                patient = Patient.query.filter_by(full_name=form.patient_full_name.data).first()
                if not patient:
                    patient = Patient(full_name=form.patient_full_name.data)
                    db.session.add(patient)
                    db.session.commit()
                session_obj = Session(
                    user_id=User.query.filter_by(email=form.doctor_email.data).first().id,
                    patient_id=patient.id,
                    doctor_email=form.doctor_email.data,
                    patient_full_name=form.patient_full_name.data,
                    session_date=form.session_date.data,
                    session_time=form.session_time.data,
                    consent=form.consent.data,
                    reason_for_visit=form.reason_for_visit.data,
                    medications=form.medications.data,
                    payment_method=form.payment_method.data,
                    total_amount=form.total_amount.data,
                    payment_status=form.payment_status.data
                )
                db.session.add(session_obj)
            db.session.commit()
            return redirect(url_for('main.sessions'))
        else:
            error = 'Form validation failed. Please check your input.'

    context = {
        'error': error,
        'form': form,
        'session_id': session_id,
        'session_obj': session_obj
    }
    return render_template('dashboard/sessions/ses_edit.html', **context)

@main.route('/calendar')
@login_required
def calendar():
    return render_template('dashboard/calendar.html')

@main.route('/documents')
@login_required
def documents():
    return render_template('dashboard/documents.html')
