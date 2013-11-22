# -*- coding: utf-8 -*-

from flask import Blueprint, request
from flask.views import MethodView

from app.shared.api import auth
from app.shared.models import JSendResponse
from app.shared.models.serialize import SerializationError
import app.blog.control as Ctrl

blog_bp = Blueprint('blog_bp', __name__)


class PostAPI(MethodView):
    """RESTful API for blog posts."""

    @auth.require_auth
    def post(self):
        """Create a new blog post."""
        try:
            post = Ctrl.create_new_blog_post(request.get_json())
        except Ctrl.BlogControlError as err:
            return JSendResponse.new_fail(err.message).jsonify(), 400

        return JSendResponse.new_success(post).jsonify(post_format='stripped')

    def get(self, post_id=None):
        """Get an existing blog post or a list of existing blog posts."""
        try:
            if post_id is not None:
                post_or_posts = Ctrl.get_blog_post_with_id(post_id)
            else:
                post_or_posts = Ctrl.get_all_blog_posts()
        except Ctrl.BlogControlError as err:
            return JSendResponse.new_fail(err.message).jsonify(), 400

        try:
            return JSendResponse.new_success(post_or_posts).jsonify(post_format=request.args.get('format', 'stripped'))
        except SerializationError as err:
            return JSendResponse.new_fail(err.message).jsonify(), 400

    @auth.require_auth
    def put(self, post_id):
        """Update an existing blog post."""
        try:
            post = Ctrl.update_blog_post_with_id(post_id, request.json)
        except Ctrl.BlogControlError as err:
            return JSendResponse.new_fail(err.message).jsonify(), 400

        return JSendResponse.new_success(post).jsonify(post_format='stripped')

    @auth.require_auth
    def delete(self, post_id):
        """Delete an existing blog post."""
        Ctrl.delete_blog_post_with_id(post_id)
        return JSendResponse.new_success().jsonify()


view = PostAPI.as_view(PostAPI.__name__.lower())
blog_bp.add_url_rule('/posts', view_func=view, methods=['GET', 'POST'])
blog_bp.add_url_rule('/posts/<int:post_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
