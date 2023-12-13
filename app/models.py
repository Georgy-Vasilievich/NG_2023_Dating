"""SQLAlchemy models"""

import flask_login
from app import db


class User(db.Model, flask_login.UserMixin):
    """Users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    location = db.Column(db.Text, nullable=True)
    user_gender = db.Column(db.Integer, default=1, nullable=False)
    preferred_genders = db.Column(db.Integer, default=0, nullable=False)
    passions = db.Column(db.Integer, default=0, nullable=False)
    additional = db.Column(db.Text)
    receive_email = db.Column(db.Boolean, default=False, nullable=False)

    def is_active(self):
        return True

    def __repr__(self):
        return " "
