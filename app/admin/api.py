# -*- coding: utf-8 -*-

from flask import Blueprint, request
from flask.views import MethodView

from app.shared.api import auth
from app.shared.models import JSendResponse
from app.admin.models import User
import app.admin.control as Ctrl

admin_bp = Blueprint('admin_bp', __name__)


@auth.verify_password
def verify_password(username_or_token, password):
    if User.verify_auth_token(username_or_token) is not None:
        return True

    try:
        user = Ctrl.get_user_with_name(username_or_token)
    except Ctrl.AdminControlException:
        return False

    return user.verify_password(password)


class UserAPI(MethodView):
    """RESTful API for users."""

    @auth.require_auth
    def post(self):
        """Create a new user."""
        user = Ctrl.create_new_user(request.get_json())
        return JSendResponse.new_success(user).jsonify()

    @auth.require_auth
    def get(self, user_id=None):
        """Get an existing user."""
        if user_id is not None:
            user_or_users = Ctrl.get_user_with_id(user_id)
        else:
            user_or_users = Ctrl.get_all_users()

        return JSendResponse.new_success(user_or_users).jsonify()

    @auth.require_auth
    def put(self, user_id):
        """Update an existing user."""
        return JSendResponse.new_fail('not implemented').jsonify(), 400

    @auth.require_auth
    def delete(self, user_id):
        """Delete an existing user."""
        return JSendResponse.new_fail('not implemented').jsonify(), 400


class LoginAPI(MethodView):
    """API endpoint for HTTP Basic Authentication."""

    @auth.require_auth
    def post(self):
        """Verify login data and respond with a new timed auth token."""
        # TODO: current user object or at least user-id
        # should be stored in session to decrease db access
        # Response should probably also include timeout (for cookie info)
        username = request.authorization.username
        try:
            user = Ctrl.get_user_with_name(username)
        except Ctrl.AdminControlException as err:
            return JSendResponse.new_error(err.message).jsonify()

        token = user.generate_auth_token()
        return JSendResponse.new_success(token.decode('ascii')).jsonify()

    @auth.require_auth
    def get(self):
        """Just check if logged in."""
        return JSendResponse.new_success('authorized').jsonify()


view = UserAPI.as_view(UserAPI.__name__.lower())
admin_bp.add_url_rule('/users', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/users/<int:user_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])

view = LoginAPI.as_view(LoginAPI.__name__.lower())
admin_bp.add_url_rule('/login', view_func=view, methods=['GET', 'POST'])
