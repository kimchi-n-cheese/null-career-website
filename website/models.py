"""This part of the program contains the database models."""
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

"""This is how the notes will be processed into the database."""
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

"""This is how the user information will be processed into the database."""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(50))
    notes = db.relationship('Note')
