from flask import Blueprint, render_template, redirect, url_for, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask.globals import request
from . import db, guard

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    req = request.get_json(force=True)
    login = req.get('email', None) if req.get('email', None) else req.get('username', None)
    password = req.get('password', None)

    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        return 'Please check your login details and try again.'
    
    gen_user_token = guard.authenticate(user.username, password)
    ret = {'access_token': guard.encode_jwt_token(gen_user_token)}

    return ret, 200

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    req = request.get_json(force=True)
    email = req.get('email', None)
    username = req.get('username', None)
    password = req.get('password', None)

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email is already exists')
        return 'Email is already exists'
    
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    gen_user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(gen_user)}

    db.session.add(new_user)
    db.session.commit()

    return ret, 200
@auth.route('/logout')
def logout():
    return 'Logout'