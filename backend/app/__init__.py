from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy, model
# from flask_praetorian import Praetorian
from flask_cors import CORS
from config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# init bcrypt
bcrypt = Bcrypt()

#init jwt
jwt = JWTManager()

#init Cors
cors = CORS()

#init Guard
# guard = Praetorian()

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
    # guard.init_app(app, models.User)
    cors.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    # Add users for the example
    with app.app_context():
        db.create_all()
        if db.session.query(models.User).filter_by(username='stray228').count() < 1:
            db.session.add(models.User(
            username='stray228',
            email='stray228@gmail.com',
            password='stray228',
            roles='admin'
                ))
        db.session.commit()

    return app