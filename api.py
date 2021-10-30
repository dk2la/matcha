import os
import flask
import flask_sqlalchemy
import flask_praetorian
import flask_cors
# import flask_mail
from flask_cors import cross_origin
from flask import json, request

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()
# mail = flask_mail.Mail()

# A generic user model that might be used by an app powered by flask-praetorian
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, index=True)
    roles = db.Column(db.Text)
    is_online = db.Column(db.Boolean, default=True, server_default='true')
    # registred_on = db.Column(db.DateTime, nullable=False)
    # confirmed = db.Column(db.Boolean, default=False, nullable=False)
    # confirmed_on = db.Column(db.DateTime, nullable=False)

    # def __init__(self, username, email, password, confirmed,
    #             paid=False, admin=False, confirmed_on=None):
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.confirmed = confirmed
    #     self.admin = admin
    #     self.confirmed_on = confirmed_on
    #     self.registred_on = registred_on


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
        return self.is_online

    def __repr__(self):
        return '<User {}>'.format(self.username)

# Initialize flask app for the example
app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

# Initialize the flask-praetorian instance for the app
guard.init_app(app, User)

# Initialize a local database for the example
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
db.init_app(app)

# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)

# Initializes Mail instance
# mail.init_app(app)


# Add users for the example
with app.app_context():
    db.create_all()
    if db.session.query(User).filter_by(username='stray228').count() < 1:
        db.session.add(User(
          username='stray228',
          password=guard.hash_password('stray228'),
          roles='admin'
            ))
    db.session.commit()


# Set up some routes for the example
@app.route('/')
@app.route('/index')
@cross_origin(supports_credentials=True)
def home():
    aboba = {"aboba": "stray228"}
    response = app.response_class(
        response=json.dumps(aboba),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/login', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"username":"Yasoob","password":"strongpassword"}'
    """
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


@app.route('/signup', methods=['POST', 'GET'])
@flask_praetorian.auth_required
@cross_origin(supports_credentials=True)
def signup():
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    email = req.get('email', None)
    


@app.route('/refresh', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200

@app.route('/protected')
@flask_praetorian.auth_required
@cross_origin(supports_credentials=True)
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}

@app.route('/me')
@flask_praetorian.auth_required
@cross_origin(supports_credentials=True)
def me():
    return {'username': flask_praetorian.current_user().username,
            'email': flask_praetorian.current_user().email,
            'roles': flask_praetorian.current_user().roles,
            'id': flask_praetorian.current_user().id,
            'is_online': flask_praetorian.current_user().is_online
            }
