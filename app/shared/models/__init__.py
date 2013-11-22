# -*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta

from flask.json import jsonify
from flask.ext.sqlalchemy import SQLAlchemy

import serialize

db = SQLAlchemy()


class JSendResponse(serialize.SerializableMixin):
    """Base class for restful JSON responses according to the JSend specification (http://labs.omniti.com/labs/jsend).

    :param status: either 'success', 'fail' or 'error'.
    :type status: str

    """
    __metaclass__ = ABCMeta

    def __init__(self, status):
        self.status = status

    @staticmethod
    def new_success(data=None):
        """Create a new 'success' response.

        :param data: optional data of the response.
        :type data: object
        :returns: DataResponse with status 'success'.

        """
        return DataResponse('success', data)

    @staticmethod
    def new_fail(data):
        """Create a new 'fail' response.

        :param data: object explaining the failure.
        :type data: object
        :returns: DataResponse with status 'fail'.

        """
        return DataResponse('fail', data)

    @staticmethod
    def new_error(message):
        """Create a new 'error' response.

        :param message: message explaining the error.
        :type message: str
        :returns: MessageResponse with status 'error'.

        """
        return MessageResponse('error', message)

    @abstractmethod
    def serializable_fields(self, **kwargs):
        return {}

    def jsonify(self, **kwargs):
        return jsonify(self.serialize(**kwargs))


class DataResponse(JSendResponse):
    """Response with a status and optional data.

    :param status: either 'success' or 'fail'
    :type status: str
    :param data: optional data of the response. Data which needs to be formatted must implement Serializable.

    """

    def __init__(self, status, data=None):
        self.data = data
        super(DataResponse, self).__init__(status)

    def serializable_fields(self, **kwargs):
        if isinstance(self.data, (serialize.SerializableMixin, list)):
            return {'status': serialize.String,
                    'data': serialize.Nested}
        else:
            return {'status': serialize.String,
                    'data': serialize.Raw}


class MessageResponse(JSendResponse):
    """Response with a status and message.

    :param status: usually 'error'
    :type status: str
    :param message: description of the error.
    :type message: str

    """

    def __init__(self, status, message):
        self.message = message
        super(MessageResponse, self).__init__(status)

    def serializable_fields(self, **kwargs):
        return {'status': serialize.String,
                'message': serialize.String}
