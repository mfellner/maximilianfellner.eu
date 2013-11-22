# -*- coding: utf-8 -*-

from app.shared.models import db
from app.blog.models import Post


def create_new_blog_post(kwargs):
    """Create a new blog post in the database.

    :param kwargs: attributes of the blog post.
    :type kwargs: dict

    """
    try:
        post = Post.new_post(**kwargs)
    except TypeError:
        raise BlogControlError('Incorrect blog post format')

    db.session.add(post)
    db.session.commit()
    return post


def get_blog_post_with_id(post_id):
    """Retrieve an existing blog post from the database.

    :param post_id: id of the blog post to retrieve.
    :type post_id: int

    """
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        raise BlogControlError('No blog post with id %d' % post_id)

    return post


def get_all_blog_posts():
    """Retrieve a list of existing blog posts from the database.

    """
    return Post.query.order_by(Post.time).all()


def update_blog_post_with_id(post_id, kwargs):
    """Update an existing blog post in the database.

    :param post_id: id of the blog post to update.
    :type post_id: int
    :param kwargs: new contents of the blog post.
    :type kwargs: dict

    """
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        raise BlogControlError('No blog post with id %d' % post_id)

    try:
        post.update_content(**kwargs)
    except TypeError:
        raise BlogControlError('Incorrect blog post format')

    db.session.add(post)
    db.session.commit()
    return post


def delete_blog_post_with_id(post_id):
    """Delete an existing blog post from the database.

    :param post_id: id of the blog post to delete.
    :type post_id: int

    """
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()


class BlogControlError(Exception):
    pass
