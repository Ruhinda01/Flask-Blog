from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from App import db, login


class User(UserMixin, db.Model):
    """A database model for users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(
        db.DateTime, default=datetime.utcnow)  # revisit

    def __repr__(self):
        return f'<user> {self.username}'

    def set_password(self, password):
        """Transforms a users password into a hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks password hash against user password"""
        return check_password_hash(self.password_hash, password)

    # creates user avatars based on users' md5 hashed email
    # that is sent to the gravatar service and returns an image
    def avatar(self, size):
        """create a user's avatar"""
        digest = md5(self.email.lower().encode('utf-8 ')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    """Creates a user loader function that 
        writess the login state to the user
        session
    """
    return User.query.get(int(id))


class Post(db.Model):
    """Model for posts"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.now)  # refer back utcnow deprecated
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<post {self.body}'
