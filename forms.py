from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from flask import request


class RegistrationForm(FlaskForm):
    enrollment_number = StringField('Enrollment No.', validators=[
        DataRequired(), Length(min=10, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField(
        'Role', choices=[('student', 'Student'), ('professor', 'Professor')])
    images = FileField('Upload Images', validators=[
                       FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])

    submit = SubmitField('Register')

    def validate(self, **kwargs):  # Add **kwargs to accept extra keyword arguments
        # Call the parent validate method with any extra arguments
        if not super(RegistrationForm, self).validate(**kwargs):
            return False
        # Check for student role
        if self.role.data == 'student':
            if not self.images.data or len(request.files.getlist("images")) != 5:
                self.images.errors.append(
                    'Students must upload exactly 5 images.')
                return False
        # Check for professor role
        elif self.role.data == 'professor':
            if not self.images.data or len(request.files.getlist("images")) != 1:
                self.images.errors.append(
                    'Professors must upload exactly 1 image.')
                return False
        return True


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ScheduleClassForm(FlaskForm):
    course = SelectField('Course', choices=[])  # Populate dynamically in route
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Schedule')
