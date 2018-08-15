# -*- coding: utf-8 -*-

import datetime
import types

from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.orm.exc import NoResultFound

from .mixins import ModelMixin, MaskableMixin





class Maskable(MaskableMixin):
    """
    A simple function like class used for masking rule.
    """

    def __call__(self, key):
        if type(key) in types.StringTypes:
            tmp_key = key.lower()
            for k in self.mask_key_has:
                if k in tmp_key:
                    return True, "'%s'" % self.mask_with
        return False, None


class ConfigError(Exception):
    """
    A error class which will be raised by the app if it's not configure properly
    """
    pass
