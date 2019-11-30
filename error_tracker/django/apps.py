# -*- coding: utf-8 -*-
#
#    Django error tracker app config
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#


from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoErrorTracker(AppConfig):
    name = 'error_tracker.django'
    label = 'error_tracker'
    verbose_name = _("Error Monitoring and Exception Tracking")
