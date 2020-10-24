# -*- coding: utf-8 -*-
#
#    Django components
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#


from .utils import DefaultDjangoContextBuilder, DjangoNotification, DefaultDjangoViewPermission
from .settings import *

from .utils import DjangoNotification, DefaultDjangoContextBuilder
from error_tracker.libs.utils import Masking, get_class_from_path, get_class_instance
from error_tracker import ModelMixin, MaskingMixin, TicketingMixin, NotificationMixin, ContextBuilderMixin, \
    ViewPermissionMixin
from django.apps import apps as django_apps
import warnings


def get_exception_model():
    """
    Return the APP error model that is active in this project.
    """
    from .models import ErrorModel
    model_path = APP_ERROR_DB_MODEL
    if model_path is None:
        warnings.warn("APP_ERROR_DB_MODEL is not set using default model")
        return ErrorModel
    try:
        return django_apps.get_model(model_path, require_ready=False)
    except ValueError:
        model = get_class_from_path(model_path, ModelMixin, raise_exception=False,
                                    warning_message="Model " + model_path + " is not importable")
        if model is not None:
            return model
        warnings.warn("APP_ERROR_DB_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        model = get_class_from_path(model_path, ModelMixin, raise_exception=False,
                                    warning_message="Model " + model_path + " is not importable")
        if model is not None:
            return model
        warnings.warn(
            "APP_ERROR_DB_MODEL refers to model '%s' that has not been installed" % model_path
        )
    raise LookupError("APP_ERROR_DB_MODEL is set to '%s' but it's not importable" % model_path)


def get_masking_module():
    return get_class_instance(APP_ERROR_MASKING_MODULE, MaskingMixin, Masking, 'Masking', APP_ERROR_MASK_WITH,
                              APP_ERROR_MASKED_KEY_HAS)


def get_ticketing_module():
    return get_class_instance(APP_ERROR_TICKETING_MODULE, TicketingMixin, None, 'Ticketing')


def get_notification_module():
    if APP_ERROR_RECIPIENT_EMAIL and APP_ERROR_EMAIL_SENDER:
        return get_class_instance(APP_ERROR_NOTIFICATION_MODULE, NotificationMixin, DjangoNotification,
                                  "Notification")


def get_context_builder():
    return get_class_instance(APP_ERROR_CONTEXT_BUILDER_MODULE, ContextBuilderMixin,
                              DefaultDjangoContextBuilder, "ContextBuilder")


def get_view_permission():
    return get_class_instance(APP_ERROR_VIEW_PERMISSION, ViewPermissionMixin, DefaultDjangoViewPermission,
                              "ViewPermission")
