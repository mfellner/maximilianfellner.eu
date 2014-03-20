# -*- coding: utf-8 -*-

from sqlalchemy.exc import IntegrityError

from app.shared.models import db
from app.admin.models import User


class AdminControlException(Exception):
    pass


def create_new_user(kwargs):
    """Create a new user in the database.

    :param kwargs: attributes of the user.
    :type kwargs: dict

    """
    if kwargs is None:
        raise AdminControlException('no arguments provided')

    user = User.new_user(**kwargs)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as err:
        raise AdminControlException(err.message)

    return user


def get_user_with_id(user_id):
    """Retrieve an existing user from the database.

    :param user_id: id of the user to retrieve.
    :type user_id: int

    """
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise AdminControlException('no user with id %d' % user_id)
    else:
        return user


def get_user_with_name(user_name):
    """Retrieve an existing user from the database.

    :param user_name: username of the user to retrieve.
    :type user_name: str

    """
    user = User.query.filter_by(name=user_name).first()

    if user is None:
        raise AdminControlException('no user with name %s' % user_name)
    else:
        return user


def get_all_users():
    """Retrieve a list of existing users from the database.

    """
    return User.query.order_by(User.name).all()
