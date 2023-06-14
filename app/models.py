from app import db
from datetime import datetime
from DBUserHandler import DBHandler
from werkzeug.security import check_password_hash, generate_password_hash

class Users(db.Model):
    UID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    FirstName = db.Column(db.String(120), nullable=False)
    LastName = db.Column(db.String(120), nullable=False)
    Username = db.Column(db.String(120), unique=True, nullable=False)
    Email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    Password = db.Column(db.String(128), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password, username):
        dbHandler = DBHandler()
        return dbHandler.attemptLogin(password, Username=username)
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    text = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    bg = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.ForeignKey(Users.UID))
    users = db.relationship(Users, backref='booking')