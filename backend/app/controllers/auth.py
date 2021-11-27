# import flask handlers
from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from flask.globals import request

# import db
from app import db

# import packages
from app.models import models
from app.handlers import handler

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    req = request.get_json(force=True)
    username = handler.get_username(req)
    password = handler.get_password(req)

    user = models.User.query.filter_by(username=username).first()
    auth = user.check_password(password)
    if not auth:
        return {'message': 'have no user'}, 401

    access_token = create_access_token(identity=str(user.id))
    ret = {'token': access_token}

    return ret, 200

@auth.route('/signup', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def signup():
    req = request.get_json(force=True)
    email = req.get('email', None)
    username = handler.get_username(req)
    password = handler.get_password(req)

    user = handler.search_data('email', email)

    if user:
        # flash('Email is already exists')
        return {'message': 'Email is already exists'}
    
    new_user = models.User(email=email, username=username, password=password)
    new_user.hash_password()
    ret = {
            'username': new_user.username,
            'email': new_user.email
        }

    db.session.add(new_user)
    db.session.commit()

    return ret, 200
    
@auth.route('/logout')
@cross_origin(supports_credentials=True)
def logout():
    return 'Logout'