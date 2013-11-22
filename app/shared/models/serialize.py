# -*- coding: utf-8 -*-


class SerializableMixin(object):
    """Mixin to provide basic data serialization."""

    def serializable_fields(self, **kwargs):
        """
        Derived classes must implement this method.
        Returns a dictionary of attribute names and field types.

        :param kwargs: optional arguments
        :type kwargs: dict

        """
        raise SerializationError('serializable_fields not implemented')

    def serialize(self, **kwargs):
        """
        Returns a dictionary with attribute names and serialized values.

        :param kwargs: optional arguments
        :type kwargs: dict
        """
        result = dict()
        for attr, field in self.serializable_fields(**kwargs).items():
            try:
                value = getattr(self, attr)
                result[attr] = field.serialize(value, **kwargs)
            except AttributeError as err:
                raise SerializationError(err.message)
        return result


class Raw(object):
    @classmethod
    def serialize(cls, value, **kwargs):
        return value


class Integer(object):
    @classmethod
    def serialize(cls, value, **kwargs):
        if value is None:
            raise SerializationError('%s value is undefined' % cls.__name__)
        try:
            return int(value)
        except ValueError as err:
            raise SerializationError(err)


class String(object):
    @classmethod
    def serialize(cls, value, **kwargs):
        if value is None:
            raise SerializationError('%s value is undefined' % cls.__name__)
        try:
            return str(value)
        except ValueError as err:
            raise SerializationError(err)


class ISODateTime(object):
    @classmethod
    def serialize(cls, value, **kwargs):
        if value is None:
            raise SerializationError('%s value is undefined' % cls.__name__)
        try:
            return value.isoformat()
        except AttributeError as err:
            raise SerializationError(err)


class Nested(object):
    @classmethod
    def serialize(cls, value, **kwargs):
        if value is None:
            raise SerializationError('%s value is undefined' % cls.__name__)
        if isinstance(value, list):
            result = []
            for v in value:
                result.append(cls._serialize(v, **kwargs))
            return result
        else:
            return cls._serialize(value, **kwargs)

    @staticmethod
    def _serialize(value, **kwargs):
        try:
            return value.serialize(**kwargs)
        except AttributeError:
            return value


class SerializationError(Exception):
    pass
