from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from forms import RegistrationForm, LoginForm
from models import User, Attendance, Course
from flask import Blueprint

# Use Blueprints for modular code
app_routes = Blueprint('app_routes', __name__)

# Homepage


@app_routes.route('/')
@app_routes.route('/home')
def home():
    return render_template('home.html')

# Registration route where file upload is handled


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard' if current_user.role == 'student' else 'professor_dashboard'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password for secure storage
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # Create a new user object (student or professor)
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        # If the user is a student, handle image uploads
        if form.role.data == 'student' and 'images' in request.files:
            images = request.files.getlist('images')

            if len(images) < 5:
                flash('Please upload at least 5 images for face recognition.', 'danger')
                return redirect(url_for('register'))

            for image in images:
                if image.filename == '':
                    flash('No image selected', 'danger')
                    return redirect(url_for('register'))

                # Secure the filename and save the image to the uploads folder
                filename = secure_filename(image.filename)
                image.save(os.path.join(Config.UPLOAD_FOLDER, filename))

            flash('Registration successful! Images uploaded.', 'success')

        else:
            flash('Registration successful!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Login route


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard' if current_user.role == 'student' else 'professor_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('student_dashboard' if user.role == 'student' else 'professor_dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', form=form)

# Logout route


@app_routes.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# Student Dashboard


@app_routes.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied', 'danger')
        return redirect(url_for('home'))

    # Fetch attendance records for the logged-in student
    attendance_records = Attendance.query.filter_by(
        student_id=current_user.id).all()

    return render_template('student_dashboard.html', attendance_records=attendance_records)

# Professor Dashboard


@app_routes.route('/professor_dashboard')
@login_required
def professor_dashboard():
    if current_user.role != 'professor':
        flash('Access denied', 'danger')
        return redirect(url_for('home'))

    # Fetch courses taught by the professor
    courses = Course.query.filter_by(professor_id=current_user.id).all()

    return render_template('professor_dashboard.html', courses=courses)

# Route to schedule a class (Professor only)


@app_routes.route('/schedule_class', methods=['POST'])
@login_required
def schedule_class():
    if current_user.role != 'professor':
        flash('Access denied', 'danger')
        return redirect(url_for('home'))

    course_id = request.form.get('course')
    date = request.form.get('date')

    # Assuming you have a method to schedule a class
    # You can add this functionality into the database here
    flash(f'Class scheduled for {date}!', 'success')
    return redirect(url_for('professor_dashboard'))

# Route to view attendance report (Professor only)


@app_routes.route('/view_report', methods=['POST'])
@login_required
def view_report():
    if current_user.role != 'professor':
        flash('Access denied', 'danger')
        return redirect(url_for('home'))

    course_id = request.form.get('course')

    # Fetch attendance records for this course
    attendance_records = Attendance.query.filter_by(course_id=course_id).all()

    return render_template('attendance_report.html', attendance_records=attendance_records)
