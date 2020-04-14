# -*- coding: utf-8 -*-
#
#     Exception formatter utils module
#
#     :copyright: 2020 Sonu Kumar
#     :license: BSD-3-Clause
#
import sys
import traceback
import warnings
from hashlib import sha256
import six

from error_tracker.libs.exception_formatter import format_exception
from error_tracker.libs.mixins import MaskingMixin


class Masking(MaskingMixin):
    """
    A simple function like class used for masking rule.
    """

    def __call__(self, key):
        if isinstance(key, six.string_types):
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


def get_exception_name(e):
    return str(e).replace("'>", "").replace("<class '", "").replace("<type 'exceptions.", "")


def get_context_detail(request, masking, context_builder,
                       additional_context):
    ty, val, tb = sys.exc_info()
    frames = traceback.format_exception(ty, val, tb)
    traceback_str = format_exception(tb, masking=masking)
    frame_str = ''.join(frames)
    rhash = sha256(str.encode(frame_str, "UTF-8")).hexdigest()
    request_data = context_builder.get_context(request, masking=masking,
                                               additional_context=additional_context)
    return ty, frames, frame_str, traceback_str, rhash, request_data


def get_notification_subject(notification_subject_prefix, method, url, exception):
    if notification_subject_prefix and method:
        subject = "[%s] [%s] %s" % (notification_subject_prefix, method, url)
    elif method:
        subject = "[%s] %s" % (method, url)
    else:
        subject = "[%s]" % notification_subject_prefix if notification_subject_prefix else ""
    if exception:
        subject = "%s %s" % (subject, exception)
    return subject


def get_class_from_path(module_path, super_class, raise_exception=True,
                        warning_message=None):
    """
    Try to import a class, that's subclass of super_class and it must have implemented all abstract methods
    :param module_path : path to the module
    :param super_class : super class
    :param raise_exception : in the case of import error, shallow it or re-raise
    :param warning_message: any warning message
    :return: imported class
    """
    from django.utils.module_loading import import_string
    try:
        cls = import_string(module_path)
        cls_fields = cls.__dict__.keys()
        matched = True
        if not issubclass(cls, super_class):
            return None
        fields = super_class.__dict__
        abstract_methods = None
        try:
            abstract_methods = cls.__abstractmethods__
        except AttributeError:
            pass
        if abstract_methods is not None:
            for method in abstract_methods:
                if method not in cls_fields:
                    matched = False
                    break
        else:
            for field, val in fields.items():
                if val is None:
                    continue
                if hasattr(val, '__isabstractmethod__'):
                    if field not in cls_fields:
                        matched = False
                        break
        if matched:
            return cls
    except ImportError as e:
        if raise_exception:
            six.reraise(ImportError, ImportError(e.message), sys.exc_info()[2])
        if warning_message:
            warnings.warn(warning_message)


def get_class_instance(module_path, mixin, default, message_prefix, *args):
    if module_path is not None:
        module = get_class_from_path(module_path, mixin,
                                     raise_exception=False,
                                     warning_message=message_prefix + " module " + module_path + " is not importable")
        if module is not None:
            return module(*args)
    if default is not None:
        message = "Default " + message_prefix + " module will be used"
        warnings.warn(message)
        return default(*args)


def get_context_dict(headers=None, context=None, form=None, args=None, masking=None):
    request_data = dict()
    form = form or {}
    headers = headers or {}
    args = args or {}
    context = context or {}
    if len(context) != 0:
        request_data['context'] = context
    if masking:
        for key in form:
            masked, value = masking(key)
            if masked:
                form[key] = value
        for key in headers:
            masked, value = masking(key)
            if masked:
                headers[key] = value
    if len(headers) != 0:
        request_data['headers'] = headers
    if len(args) != 0:
        request_data['args'] = args
    if len(form) != 0:
        request_data['form'] = form
    return request_data
