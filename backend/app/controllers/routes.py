from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import db, models

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/index')
@cross_origin(supports_credentials=True)
def index():
    return {'rabotay': 'chert'}

@routes.route('/profile')
@jwt_required()
@cross_origin(supports_credentials=True)
def profile():
    return {'pishi code blyat': 'chert blyat'}
