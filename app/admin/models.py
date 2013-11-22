# -*- coding: utf-8 -*-

from flask import current_app
from passlib.context import CryptContext
from itsdangerous import TimedJSONWebSignatureSerializer as SignatureSerializer, SignatureExpired, BadSignature

from app.shared.models import db
from app.shared.models import serialize

crypt_context = CryptContext(schemes=['pbkdf2_sha512'], default='pbkdf2_sha512')


class User(db.Model, serialize.SerializableMixin):
    """Model class for a user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(32), index=True, unique=True)
    hash = db.Column(db.String(130))

    def __init__(self, name):
        self.name = name.strip().lower()
        self.hash = None
        self.salt = None

    def set_password(self, password):
        self.hash = User.hash_password(password)

    def verify_password(self, password):
        return crypt_context.verify(password, self.hash)

    def generate_auth_token(self, expiration=600):
        s = SignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = SignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def hash_password(password):
        return crypt_context.encrypt(password)

    @staticmethod
    def new_user(name, password):
        """Create a new user.

        :param name: username.
        :type name: str
        :param password: plain text password.
        :type password: str

        """
        user = User(name)
        user.set_password(password)
        return user

    def serializable_fields(self):
        return {'id': serialize.Integer,
                'name': serialize.String}
