from enum import unique
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True, index=True)
    username = db.Column(db.String, unique=True, nullable=True, index=True)
    password = db.Column(db.String)
    roles = db.Column(db.Text, default='user')
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, password=password, email=email, username=username):
        self.password = password
        self.username = username
        self.email = email

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return ["Have no role"]

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    
    