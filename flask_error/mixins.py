# -*- coding: utf-8 -*-

class MaskableMixin(object):

    def __init__(self, mask_with, mask_key_has):
        """
        :param mask_with: masked value to be used for a given variable
        :param mask_key_has: tuple of strings to be used for checking masking rule
        """
        self.mask_key_has = mask_key_has
        self.mask_with = mask_with

    def __call__(self, key):
        raise NotImplementedError


class ModelMixin(object):
    """
    Base interface for data mode which can be used to store data in MongoDB/MySQL or any other data store.
    """
    hash = None
    host = None
    path = None
    method = None
    request_data = None
    exception = None
    count = None
    created_on = None
    last_seen = None

    def __str__(self):
        return "'%s' '%s' %s" % (self.host, self.path, self.count)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return "ModelMixin(%s)" % self.__str__()

    @classmethod
    def delete(cls, rhash):
        """
        :param rhash: lookup key
        :return: None
        """
        raise NotImplementedError

    @classmethod
    def create_or_update(cls, rhash, host, path, method, request_data, exception):
        """
        :param rhash: Key of the db entry
        :param host: App host e.g. example.com
        :param path: request path
        :param method: request method (GET/POST/PUT etc)
        :param request_data: request form data
        :param exception: Exception data captured
        :return:  None
        """
        raise NotImplementedError

    @classmethod
    def get_all(cls):
        """
        :return: All entries from the store
        """
        raise NotImplementedError

    @classmethod
    def get(cls, rhash):
        """
        :param rhash: key for lookup
        :return: Single entry of this class
        """
        raise NotImplementedError


class MailMixin(object):
    """
    A mail mixin class which can be used to send any kind of mail.
    """

    def __init__(self, *args, **kwargs):
        pass

    def send(self, message):
        raise NotImplementedError
