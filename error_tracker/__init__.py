# -*- coding: utf-8 -*-
#
#    Error Tracking app
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

__version__ = '2.1.0'
__author__ = 'Sonu Kumar'
__email__ = 'sonunitw12@gmail.com'

from error_tracker.libs.mixins import *
from error_tracker.libs.exception_formatter import *

flaskInstalled = False
try:
    import flask

    flaskInstalled = True
except ImportError:
    pass

if flaskInstalled:
    from error_tracker.flask import *
    from error_tracker.flask.utils import configure_scope as flask_scope

djangoInstalled = False
try:
    import django

    djangoInstalled = True
except ImportError as e:
    raise e

if djangoInstalled:
    from error_tracker.django import *
    from error_tracker.django.apps import DjangoErrorTracker
    from error_tracker.django.utils import capture_message, track_exception, configure_scope, capture_exception

__all__ = [
    # flask modules
    "AppErrorTracker", "DefaultFlaskContextBuilder", "flask_scope",

    # mixin classes
    "NotificationMixin", "ModelMixin", "MaskingMixin",
    "ContextBuilderMixin", "TicketingMixin", "ViewPermissionMixin",

    # Django modules
    "DefaultDjangoContextBuilder", "DjangoErrorTracker", "DefaultDjangoViewPermission",
    "capture_message", "track_exception", "configure_scope", "capture_exception",

    # lower level methods
    "format_exception", "print_exception"
]
