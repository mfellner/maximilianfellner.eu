# -*- coding: utf-8 -*-

"""empty message

Revision ID: 4e0fa38e69af
Revises: None
Create Date: 2014-03-05 22:27:48.363295

"""

import random
import logging

from alembic import op
from sqlalchemy.sql import table
import sqlalchemy as sa

from app.admin.models import User

# Revision identifiers, used by Alembic.
revision = '4e0fa38e69af'
down_revision = None


def upgrade():
    # Create blog posts table.
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.Unicode(length=32), nullable=True),
    sa.Column('title', sa.Unicode(length=128), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('time', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # Create users table.
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=32), nullable=True),
    sa.Column('hash', sa.String(length=130), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_name', 'users', ['name'], unique=True)

    users = table('users',
     sa.Column('id', sa.Integer()),
     sa.Column('name', sa.Unicode(length=32)),
     sa.Column('hash', sa.String(length=130))
    )

    # Generate initial 'root' user.
    password = '%08x' % random.randrange(16**8)
    hash = User.hash_password(password)
    op.bulk_insert(users, [{'name': u'root', 'hash': hash}])
    logging.getLogger('alembic.migration').info('Generated user "root" with password %s', password)


def downgrade():
    op.drop_index('ix_user_name', table_name='users')
    op.drop_table('users')
    op.drop_table('posts')
