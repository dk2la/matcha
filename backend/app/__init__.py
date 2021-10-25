from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_praetorian import Praetorian

# Initialize application
app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

# Initialize cors
cors = CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)

# Initialize guard
guard = Praetorian(app)

# Initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models

with app.app_context():
    db.create_all()
    if db.session.query(models.User).filter_by(username='stray228').count() < 1:
        db.session.add(models.User(
          username='stray228',
          password=guard.hash_password('stray228'),
          roles=2
            ))
    db.session.commit()