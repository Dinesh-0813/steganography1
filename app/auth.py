from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models import User
from app import db
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('main.dashboard'))
        
        flash('Please check your login details and try again.', 'danger')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')

            # Check if user already exists
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists', 'danger')
                return redirect(url_for('auth.register'))

            # Create new user
            new_user = User()
            new_user.email = email
            new_user.username = username
            new_user.set_password(password)

            # Add to database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))

        return render_template('auth/register.html')  # Make sure this path is correct
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        flash('An error occurred during registration', 'danger')
        return render_template('auth/register.html')  # Return template instead of redirect on error
        return redirect(url_for('auth.register'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))