# -*- coding: utf-8 -*-
#
#    Django error tracker utils classes
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

import json
import re

from error_tracker.libs.mixins import ContextBuilderMixin, NotificationMixin, ViewPermissionMixin
from error_tracker.libs.utils import get_context_dict

from django.core.mail import send_mail
from django.http import RawPostDataException


class DefaultDjangoContextBuilder(ContextBuilderMixin):
    """
    Default request builder, this records, form data, header and URL parameters and mask them if necessary
    """

    @staticmethod
    def _get_form_data(request):
        form = {}
        if request is None:
            return form
        post = request.POST
        if post is None or len(post) == 0:
            body = None
            try:
                body = request.data
            except AttributeError:
                try:
                    body = request.body
                except RawPostDataException:
                    pass
            if body is not None:
                try:
                    from rest_framework.request import Request
                    if isinstance(body, Request):
                        form = body.data
                except ImportError:
                    pass
                if len(form) == 0 and len(body) > 0:
                    try:
                        form = json.loads(body, encoding="UTF-8")
                    except Exception:
                        form = {'data': body}
        else:
            form = post.dict()
        return form

    @staticmethod
    def _get_headers(request):
        return _HeaderExtractor(request).get_headers()

    @staticmethod
    def _get_args(request):
        if request is not None:
            return request.GET.dict()

    def get_context(self, request, masking=None, additional_context=None):
        return str(get_context_dict(headers=self._get_headers(request),
                                    form=self._get_form_data(request),
                                    args=self._get_args(request),
                                    context=additional_context,
                                    masking=masking))


class DjangoNotification(NotificationMixin):
    """
    Send emails to the configured users
    """

    def notify(self, request, exception,
               email_subject=None,
               email_body=None,
               from_email=None,
               recipient_list=None):
        if recipient_list is not None and from_email is not None:
            send_mail(email_subject, email_body, from_email, recipient_list, fail_silently=True)
            exception.notification_sent = True
            exception.save()


class DefaultDjangoViewPermission(ViewPermissionMixin):

    def __call__(self, request):
        if hasattr(request.user, "is_superuser"):
            return request.user.is_superuser
        return False


class configure_scope(object):
    """
    Use this class to work with context manager where more context can be added on the fly

    usage
    with configure_scope(request=request) as scope:
        scope.set_extra("id", 1234)

    """

    def __init__(self, request=None, handle_exception=True, context=None):
        """
        :param request:  current request object
        :param handle_exception:  whether exception has to be re-raised or not
        :param context: initial context detail
        """
        self.context = context or {}
        self.request = request
        self.handle_exception = handle_exception

    def set_extra(self, key, value):
        """
        Add key value in context detail
        :param key:  context key
        :param value: context value
        :return:
        """
        self.context[key] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            capture_exception(request=self.request,
                              exception=exc_type,
                              additional_context=self.context)
        return self.handle_exception


def capture_message(message, exception=None, request=None):
    """
    Use this method to capture any message once exception is excepted
    :param message:  message to be recorded
    :param exception:  exception occurred
    :param request:  current request object
    :return:  None
    """
    return capture_exception(request=request, exception=exception,
                             additional_context={'message': message})


def track_exception(func, additional_context=None, request=None, silent=False):
    """
    Decorator to be used for automatic exception capture
    :param func:  function on which it has been used
    :param additional_context:  additional context detail
    :param request:  current request
    :param silent: exception should be re-raised or not
    :return: None
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            capture_exception(request=request, exception=ex, additional_context=additional_context)
            if not silent:
                raise ex

    return wrapper


def capture_exception(request=None, exception=None, additional_context=None):
    """
    Use this method to capture any exception after it has been captured using try except
    :param exception:  exception occurred
    :param request:  current request object
    :param additional_context: any additional context detail
    :return:  None
    """
    from error_tracker.django.middleware import error_tracker
    error_tracker.capture_exception(request=request, exception=exception,
                                    additional_context=additional_context)


def clean_value(x):
    x = x.value.replace('[["', "").replace('"]]', "").replace('"', "")
    return x


class _HeaderExtractor(object):
    ignored_keys = frozenset(['sec_ch_ua'])
    regex = re.compile('^HTTP_')

    def __init__(self, request):
        self.request = request

    def _get_raw_headers(self):
        if self.request is None:
            return {}
        try:
            return self.request.headers
        except AttributeError:
            return dict((self.regex.sub('', header), value) for (header, value)
                        in self.request.META.items() if header.startswith('HTTP_'))

    def _can_be_skipped(self, header_name, header_value):
        return header_name.lower() in self.ignored_keys

    def get_headers(self):
        headers = self._get_raw_headers()
        new_headers = {}
        for key, value in headers.items():
            if self._can_be_skipped(key, value):
                continue
            new_headers[key] = self.get_value(key, value)
        return new_headers

    @staticmethod
    def get_value(key, value):
        try:
            # Parse each key, value from headers items and Test if could be "json loaded".
            # If not, we set the correspondent value to empty except for cookie key.
            json.loads('{"%s":"%s"}' % (key, value))
        except Exception as e:
            if key.lower() == "cookie":
                try:
                    from http.cookies import SimpleCookie
                    try:
                        cookie = SimpleCookie()
                        cookie.load(value)
                        value = {k: clean_value(v) for k, v in cookie.items()}
                    except Exception as e:
                        value = ""
                except ImportError:
                    pass
            else:
                value = ""
        return value
