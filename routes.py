from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db, bcrypt  # Import from extensions
from forms import RegistrationForm, LoginForm
from models import User, Attendance, Course, Classroom
import os
from config import Config
from werkzeug.utils import secure_filename

# Blueprint for routes
app_routes = Blueprint('app_routes', __name__)

# Define routes here...

# Homepage


@app_routes.route('/')
@app_routes.route('/home')
def home():
    return render_template('home.html')

# Registration route where file upload is handled


@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    print("Registration route hit")  # Debugging: Route hit

    if current_user.is_authenticated:
        print(
            f"User {current_user.username} is already authenticated with role {current_user.role}")
        return redirect(url_for('app_routes.student_dashboard' if current_user.role == 'student' else 'app_routes.professor_dashboard'))

    form = RegistrationForm()
    print("Form instantiated")  # Debugging: Form instantiated

    if form.validate_on_submit():
        print("Form validated successfully")  # Debugging: Form validated

        # Check for existing user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            # Debugging: Existing email
            print(f"User with email {form.email.data} already exists")
            flash(
                'Email already registered. Please choose a different one or log in.', 'danger')
            return redirect(url_for('app_routes.register'))

        # Hash the password for secure storage
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # Debugging: Password hashed
        print(f"Password hashed for user {form.username.data}")

        # Create a new user object (student or professor)
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        # Debugging: User added to DB
        print(
            f"User {form.username.data} with role {form.role.data} added to the database")

        # If the user is a student, handle image uploads
        if form.role.data == 'student' and 'images' in request.files:
            images = request.files.getlist('images')
            # Debugging: Images received
            print(f"Student role selected, {len(images)} images received")

            if len(images) < 5:
                # Debugging: Not enough images
                print("Fewer than 5 images uploaded for student")
                flash('Please upload at least 5 images for face recognition.', 'danger')
                return redirect(url_for('app_routes.register'))

            for image in images:
                if image.filename == '':
                    print("No image selected")  # Debugging: No image selected
                    flash('No image selected', 'danger')
                    return redirect(url_for('app_routes.register'))

                # Secure the filename and save the image to the uploads folder
                filename = secure_filename(image.filename)
                image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                # Debugging: Image saved
                print(f"Image {filename} saved for student")

            flash('Registration successful! Images uploaded.', 'success')

        # For professors, handle the single image upload
        elif form.role.data == 'professor' and 'images' in request.files:
            images = request.files.getlist('images')
            # Debugging: Image received
            print(f"Professor role selected, {len(images)} image(s) received")

            if len(images) != 1:
                # Debugging: Wrong number of images
                print("Incorrect number of images uploaded for professor")
                flash('Professors must upload exactly 1 image.', 'danger')
                return redirect(url_for('app_routes.register'))

            image = images[0]  # Since professor uploads only one image
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            # Debugging: Image saved
            print(f"Image {filename} saved for professor")

            flash('Registration successful! Image uploaded.', 'success')

        else:
            # Debugging: No images uploaded
            print("No images uploaded, proceeding without image upload")
            flash('Registration successful!', 'success')

        return redirect(url_for('app_routes.login'))

    print("Form did not validate")  # Debugging: Form validation failed
    print(form.errors)  # Debugging: Form errors
    return render_template('register.html', form=form)

# Login route


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app_routes.student_dashboard' if current_user.role == 'student' else 'app_routes.professor_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('app_routes.student_dashboard' if user.role == 'student' else 'app_routes.professor_dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', form=form)

# Logout route


@app_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('app_routes.home'))


# Student Dashboard route

@app_routes.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied', 'danger')
        return redirect(url_for('app_routes.home'))

    # Fetch all courses the student has ever attended
    courses = db.session.query(Course).join(Attendance).filter(
        Attendance.student_id == current_user.id).all()

    attendance_summary = []
    for course in courses:
        total_classes = db.session.query(Attendance).filter_by(
            course_id=course.id).count()

        attended_classes = db.session.query(Attendance).filter_by(
            course_id=course.id, student_id=current_user.id, status='Present').count()

        missed_classes = total_classes - attended_classes  # Calculate missed classes

        if total_classes > 0:
            attendance_percentage = (attended_classes / total_classes) * 100
        else:
            attendance_percentage = 0

        attendance_summary.append({
            'course': {
                'id': course.id,
                'name': course.name
            },
            'attended': attended_classes,
            'missed': missed_classes,
            'percentage': attendance_percentage
        })

    return render_template('student_dashboard.html', attendance_summary=attendance_summary)

# Route for viewing detailed attendance of a particular course


@app_routes.route('/course/<int:course_id>/attendance')
@login_required
def view_attendance(course_id):
    if current_user.role != 'student':
        flash('Access denied', 'danger')
        return redirect(url_for('app_routes.home'))

    course = Course.query.get_or_404(course_id)

    # Fetch attendance records for this course for the current user
    attendance_records = Attendance.query.filter_by(
        course_id=course_id, student_id=current_user.id).all()

    return render_template('course_attendance.html', course=course, attendance_records=attendance_records)


# Professor Dashboard

@app_routes.route('/professor_dashboard')
@login_required
def professor_dashboard():
    if current_user.role != 'professor':
        flash('Access denied', 'danger')
        return redirect(url_for('app_routes.home'))

    # Fetch courses and classrooms from the database
    courses = Course.query.filter_by(professor_id=current_user.id).all()
    classrooms = Classroom.query.all()  # Fetch all classrooms

    return render_template('professor_dashboard.html', courses=courses, classrooms=classrooms)


# Route to schedule a class


@app_routes.route('/schedule_class', methods=['POST'])
@login_required
def schedule_class():
    if current_user.role != 'professor':
        flash('Access denied', 'danger')
        return redirect(url_for('app_routes.home'))

    course_id = request.form.get('course')
    classroom_id = request.form.get('classroom')  # Get the selected classroom
    date = request.form.get('date')

    # Use the classroom_id and course_id as needed (e.g., save to the database or perform an action)

    flash(f'Class scheduled in classroom {classroom_id} for {date}!', 'success')
    return redirect(url_for('app_routes.professor_dashboard'))


# Route to view attendance report (Professor only)


@app_routes.route('/view_report', methods=['POST'])
@login_required
def view_report():
    if current_user.role != 'professor':
        flash('Access denied', 'danger')
        return redirect(url_for('app_routes.home'))

    course_id = request.form.get('course')

    # Fetch attendance records for this course
    attendance_records = Attendance.query.filter_by(course_id=course_id).all()

    return render_template('attendance_report.html', attendance_records=attendance_records)



