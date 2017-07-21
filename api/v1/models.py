import os
from api import db,create_app
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt

class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist', backref="User", order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """Initialize a user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def is_valid(self, password):
        """ This method validates a user's password """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """This method saves a user into the database"""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ This method uses jwt to generate the access token"""
        app = create_app(config_name=os.getenv('APP_SETTINGS'))
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """ This method uses jwt to decode the access token from the Authorization header."""
        app = create_app(config_name=os.getenv('APP_SETTINGS'))
        try:
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    items = db.relationship('Items', backref="Bucketlist", cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """initialize with name."""
        self.name = name
        self.created_by = created_by

    def save(self):
        """This method saves a new bucketlist item into the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id, limit, page, search_param):
        """This method queries the database and returns all the the bucketlist items
            belonging to a specific user.
        """
        if search_param:
            return Bucketlist.query.filter_by(created_by=user_id).filter(
                Bucketlist.name.ilike('%' + search_param + '%')).paginate(page, limit, False)
        else:
            return Bucketlist.query.filter_by(created_by=user_id).paginate(page, limit, False)


    def delete(self):
        """This method deletes a bucketlist from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class Items(db.Model):
    __tablename__ = 'BucketlistItems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    done = db.Column(db.Boolean)

    def __init__(self, name, id):
        self.name = name
        self.bucketlist_id = id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """This method deletes a bucketlist item from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Items {}'.format(self.name)

