# -*- coding: utf-8 -*-

from datetime import datetime

from app.shared.models import db
from app.shared.models import serialize


class Post(db.Model, serialize.SerializableMixin):
    """Model class for a blog post."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Unicode(32))
    title = db.Column(db.Unicode(128))
    content = db.Column(db.UnicodeText())
    time = db.Column(db.DateTime(timezone=True))

    def __init__(self):
        self.author = u''
        self.time = datetime.utcnow()
        self.title = u''
        self.content = u''

    def update_content(self, author=None, title=None, content=None, time=False):
        """Update contents of the blog post.

        :param author: new author of the post.
        :type author: str
        :param title: new title of the post.
        :type title: str
        :param content: new text of the post.
        :type content: str
        :param time: wether to update the timestamp.
        :type content: bool

        """
        self.author = author or self.author
        self.title = title or self.title
        self.content = content or self.content
        if time is True:
            self.time = datetime.utcnow()

    @classmethod
    def new_post(cls, author=u'', title=u'', content=u''):
        """Create a new blog post. The creation time will be set to the current UTC time.

        :param author: author of the post (may be empty).
        :type author: str
        :param title: title of the post (may be empty).
        :type title: str
        :param content: text of the post (may be empty).
        :type content: str

        """
        post = cls()
        post.author = author
        post.title = title
        post.content = content
        return post

    def serializable_fields(self, **kwargs):
        post_format = kwargs.get('post_format', 'stripped')
        if post_format == 'stripped':
            return {'id': serialize.Integer,
                    'author': serialize.String,
                    'time': serialize.ISODateTime,
                    'title': serialize.String}
        elif post_format == 'full':
            return {'id': serialize.Integer,
                    'author': serialize.String,
                    'time': serialize.ISODateTime,
                    'title': serialize.String,
                    'content': serialize.String}
        else:
            raise serialize.SerializationError('Unexpected post format \'%s\'' % post_format)
