# -*- coding: utf-8 -*-
#
#    Error Tracking app
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

__version__ = '1.1.6'
__author__ = 'Sonu Kumar'
__email__ = 'sonunitw12@gmail.com'

from error_tracker.libs.mixins import *
from error_tracker.flask import *
from error_tracker.django import *
from error_tracker.flask.utils import configure_scope as flask_scope
from error_tracker.django.apps import DjangoErrorTracker
from error_tracker.django.utils import capture_message, track_exception, configure_scope, capture_exception
from error_tracker.libs.exception_formatter import *

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
