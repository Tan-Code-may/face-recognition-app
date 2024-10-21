from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField(
        'Role', choices=[('student', 'Student'), ('professor', 'Professor')])
    images = FileField('Upload Images (for students)', validators=[
                       DataRequired()])  # Only if student selected
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ScheduleClassForm(FlaskForm):
    course = SelectField('Course', choices=[])  # Populate dynamically in route
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Schedule')
