from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User:
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def __init__(self, password=None):
        self.password = password

    def __repr__(self):
        return '<User %s>' % self.username


    @property
    def password(self):
        raise AttributeError('password is notr a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name
