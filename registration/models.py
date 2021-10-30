class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registred_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, confirmed,
                    paid=False, admin=False, confirmed_on=None):
            self.username = username
            self.email = email
            self.password = password
            self.confirmed = confirmed
            self.admin = admin
            self.confirmed_on = confirmed_on
            self.registred_on = registred_on

