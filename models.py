from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "student" or "professor"

    # For students: link to attendance records
    attendance_records = db.relationship(
        'Attendance', backref='student', lazy=True)

    # For professors: link to the courses they teach
    courses = db.relationship('Course', backref='professor', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Link to attendance records for this course
    attendance_records = db.relationship(
        'Attendance', backref='course', lazy=True)

    def __repr__(self):
        return f"Course('{self.name}', Professor ID: {self.professor_id})"


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False)  # "Present" or "Absent"
    student_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)

    def __repr__(self):
        return f"Attendance(Student ID: {self.student_id}, Course ID: {self.course_id}, Status: {self.status})"

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=True)  # Optional: location of the classroom
    capacity = db.Column(db.Integer, nullable=True)  # Optional: capacity of the classroom

    def __repr__(self):
        return f"Classroom('{self.name}', Capacity: {self.capacity}, Location: {self.location})"