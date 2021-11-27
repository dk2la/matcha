from flask.globals import request
from typing import Dictionary, List, NamedTuple
from . import db
from app.models import models

def get_username(req):
    username = req.get('username', None)
    return username

def get_password(req):
    password = req.get('password', None)
    return password

def search_data(current_field_db, current_field_user):
    data = models.User.query.filter_by(current_field_db=current_field_user).first()
    return data

def get_match(current_user) -> Dictionary:
    matches = dict()
    list_matches = models.User.query.filter_by(matches=current_user).all()
    for m in list_matches:
        matches += {}
