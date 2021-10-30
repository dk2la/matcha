from flask import Blueprint
from . import db

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/index')
def index():
    return 'Index'

@routes.route('/profile')
def profile():
    return 'Profile'

