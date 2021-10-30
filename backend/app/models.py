from enum import unique
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True, index=True)
    username = db.Column(db.String, unique=True, nullable=True, index=True)
    password = db.Column(db.String, nullable=True)
    roles = db.Column(db.Text, default='user')
    is_active = db.Column(db.Boolean, default=False)

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

    def __repr__(self):
        return '<User {}>'.format(self.username)

    
    