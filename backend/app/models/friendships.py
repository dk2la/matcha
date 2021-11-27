from enum import unique
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db
from . import models

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user = db.Column(db.Integer, db.ForeignKey('models.user.id'), primary_key=True)
    second_user = db.Column(db.Integer, db.ForeignKey('models.user.id'), primary_key=True)
    status = db.Column(db.Boolean, default=False)

    def accept_invintation():
        print('aboba')
    
    def reject_invintation():
        print('aboba')
