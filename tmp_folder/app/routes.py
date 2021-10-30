from flask import render_template, flash, redirect, url_for, request, flask_praetorian
# from wtforms.fields.simple import PasswordField
from app import app, guard
# from app.form import LoginForm
from flask_cors import cross_origin
from flask import json


@app.route('/')
@app.route('/index')
@cross_origin(supports_credentials=True)
def index():
    # user = {'username': 'Danila'}
    # return render_template('index.html', title='Aboba', user=user)
    aboba = {"aboba": "stray228"}
    response = app.response_class(
        response=json.dumps(aboba),
        status=200,
        mimetype='application/json'
    )
    return response


# @app.route('/login', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
#         return redirect(url_for('/index'))
#     return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def login():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


@app.route('/protected')
@flask_praetorian.auth_required
def protected():
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}


@app.route('/me')
@flask_praetorian.auth_required
def me():
    return {'name': flask_praetorian.current_user().username,
            'email': flask_praetorian.current_user().email,
            'roles': flask_praetorian.current_user().roles
            }
