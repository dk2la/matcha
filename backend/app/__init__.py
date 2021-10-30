from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from config import Config

#init Guard
guard = Praetorian()

# init SQLAlchemy
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # if test_config == None:
    #     app.config.mapping(
    #         SECRET_KEY='dev'
    #     )

    app.config.from_object(Config)
    app.debug = True

    from . import models, db

    db.init_app(app)
    guard.init_app(app, models.User)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app