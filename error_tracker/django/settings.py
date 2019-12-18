# -*- coding: utf-8 -*-
#
#    Django error tracker default settings
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

from django.conf import settings as dj_settings
from django.core.exceptions import ImproperlyConfigured


def get(key, default):
    try:
        return getattr(dj_settings, key, default)
    except ImproperlyConfigured:
        return default


# App's HOME page default page size
EXCEPTION_APP_DEFAULT_LIST_SIZE = get('EXCEPTION_APP_DEFAULT_LIST_SIZE', 20)
# what all sensitive data should be masked, this means any variables whose name have
# either password or secret would be masked
APP_ERROR_MASKED_KEY_HAS = get('APP_ERROR_MASKED_KEY_HAS', ("password", "secret"))
# Sensitive data masking value
APP_ERROR_MASK_WITH = get('APP_ERROR_MASK_WITH', '*************')
# exception email subject prefix
APP_ERROR_SUBJECT_PREFIX = get('APP_ERROR_SUBJECT_PREFIX', '')
# whose email would be used to send email
APP_ERROR_EMAIL_SENDER = get('APP_ERROR_EMAIL_SENDER', None)
# whom email should be send in the case of failure
APP_ERROR_RECIPIENT_EMAIL = get('APP_ERROR_RECIPIENT_EMAIL', None)
# Whether all types of errors should be tracked or not e.g. 404, 401 etc
TRACK_ALL_EXCEPTIONS = get('TRACK_ALL_EXCEPTIONS', False)
# Path to masking module
APP_ERROR_MASKING_MODULE = get('APP_ERROR_MASKING_MODULE', None)
# path to ticketing module, it should not have any constructor parameters
APP_ERROR_TICKETING_MODULE = get('APP_ERROR_TICKETING_MODULE', None)
# path to notifier module, that would send notifications to entities
APP_ERROR_NOTIFICATION_MODULE = get('APP_ERROR_NOTIFICATION_MODULE', None)
# path to custom context builder
APP_ERROR_CONTEXT_BUILDER_MODULE = get('APP_ERROR_CONTEXT_BUILDER_MODULE', None)
# In case of different database model, provide path to that
APP_ERROR_DB_MODEL = get('APP_ERROR_DB_MODEL', None)
# Check error views are visible to others or not
APP_ERROR_VIEW_PERMISSION = get('APP_ERROR_VIEW_PERMISSION', None)
