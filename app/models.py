from flask_login import UserMixin, current_user
from sqlalchemy import event
from app import db, login
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    position = db.Column(db.String(64))  # New attribute: Position
    department = db.Column(db.String(64))  # New attribute: Department

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(128))
    path = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Document {self.file_name}>'

# Define event listener functions to set created_by and updated_by
@event.listens_for(Document, 'before_insert')
def set_created_by(mapper, connection, target):
    target.created_by = current_user.id if current_user.is_authenticated else None

@event.listens_for(Document, 'before_update')
def set_updated_by(mapper, connection, target):
    target.updated_by = current_user.id if current_user.is_authenticated else None
