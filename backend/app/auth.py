from flask import Blueprint, render_template, redirect, url_for, jsonify, flash
from .models import User
from flask.globals import request
from . import db
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    req = request.get_json(force=True)
    # req.get('email', None) if req.get('email', None) else 
    username = req.get('username', None)
    password = req.get('password', None)

    user = User.query.filter_by(username=username).first()
    auth = user.check_password(password)
    if not auth:
        return {'message': 'have no user'}, 401

    access_token = create_access_token(identity=str(user.id))
    # gen_user_token = guard.authenticate(username, password)
    # ret = {'access_token': guard.encode_jwt_token(gen_user_token)}
    ret = {'token': access_token}

    return ret, 200

@auth.route('/signup', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def signup():
    req = request.get_json(force=True)
    email = req.get('email', None)
    username = req.get('username', None)
    password = req.get('password', None)

    user = User.query.filter_by(email=email).first()

    if user:
        # flash('Email is already exists')
        return {'message': 'Email is already exists'}
    
    new_user = User(email=email, username=username, password=password)
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