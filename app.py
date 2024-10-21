from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, User, Attendance, Course  # Explicit imports from models
from forms import RegistrationForm, LoginForm
import os
from config import Config  # Import the config class

app = Flask(__name__)

# Load configuration from the Config class
app.config.from_object(Config)

# Initialize database, bcrypt, and login manager after configuration is set
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Homepage route


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# Registration route


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('professor_dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

# Student dashboard


@app.route("/student_dashboard")
@login_required
def student_dashboard():
    # Show attendance data for the logged-in student
    attendance = Attendance.query.filter_by(student_id=current_user.id).all()
    return render_template('student_dashboard.html', attendance=attendance)

# Professor dashboard


@app.route("/professor_dashboard")
@login_required
def professor_dashboard():
    # Show professor options
    return render_template('professor_dashboard.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
