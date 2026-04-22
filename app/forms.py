from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

NIGERIAN_STATES = [
    ('', '-- Select State --'),
    ('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'),
    ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('FCT', 'FCT - Abuja'),
    ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'),
    ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'),
    ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara')
]

COURSES = [
    ('', '-- Select Course --'),
    ('Computer Science', 'Computer Science'),
    ('Computer Engineering', 'Computer Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Accounting', 'Accounting'),
    ('Business Administration', 'Business Administration'),
    ('Economics', 'Economics'),
    ('Mass Communication', 'Mass Communication'),
    ('Medicine and Surgery', 'Medicine and Surgery'),
    ('Pharmacy', 'Pharmacy'),
    ('Law', 'Law'),
    ('Architecture', 'Architecture'),
    ('Statistics', 'Statistics'),
    ('Mathematics', 'Mathematics'),
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('Biochemistry', 'Biochemistry'),
    ('Microbiology', 'Microbiology'),
    ('Agricultural Science', 'Agricultural Science'),
    ('Nursing Science', 'Nursing Science'),
    ('Information Technology', 'Information Technology'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Software Engineering', 'Software Engineering'),
]

OPPORTUNITY_TYPES = [
    ('', '-- Select Type --'),
    ('SIWES Placement', 'SIWES Placement'),
    ('Graduate Job', 'Graduate Job'),
]

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    course = SelectField('Course of Study', choices=COURSES, validators=[DataRequired()])
    state = SelectField('State of Location', choices=NIGERIAN_STATES, validators=[DataRequired()])
    opportunity_type = SelectField('What are you looking for?', choices=OPPORTUNITY_TYPES, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')