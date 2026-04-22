from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    course = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    opportunity_type = db.Column(db.String(50), nullable=False)  # 'SIWES Placement' or 'Graduate Job'
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Organisation(db.Model):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sector = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    relevant_courses = db.Column(db.Text, nullable=False)  # comma-separated courses
    opportunity_type = db.Column(db.String(50), nullable=False)  # 'SIWES Placement' or 'Graduate Job'
    website = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Organisation {self.name}>'