# -*- coding: utf-8 -*-
#
#    Django error tracker default urls
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

from django.urls import path
from .views import detail, view_list, delete_exception

app_name = 'error_tracker'
urlpatterns = [
    path('', view_list, name="view_errors"),
    path('<rhash>/delete', delete_exception, name='delete_error'),
    path('<rhash>', detail, name='view_error'),
]
