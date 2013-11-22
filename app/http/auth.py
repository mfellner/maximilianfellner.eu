# -*- coding: utf-8 -*-

from functools import wraps

from flask import request


class HTTPBasicAuth(object):
    """Basic HTTP authentication scheme."""

    def __init__(self):
        self.verify_password_hook = self._raise_undefined
        self.unauthorized_hook = self._raise_undefined

    def require_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.verify_password_hook(auth.username, auth.password):
                return self.unauthorized_hook()
            return f(*args, **kwargs)

        return decorated

    def verify_password(self, f):
        self.verify_password_hook = f

    def unauthorized(self, f):
        self.unauthorized_hook = f

    @staticmethod
    def _raise_undefined(*args, **kwargs):
        raise UndefinedHooks('HTTPBasicAuth hook is undefined.')


class UndefinedHooks(Exception):
    pass
