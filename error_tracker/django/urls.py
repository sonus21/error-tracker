# -*- coding: utf-8 -*-
#
#    Django error tracker default urls
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

from django.conf.urls import url
from .views import detail, view_list, delete_exception

urlpatterns = [
    url(r'^$', view_list, name="view_errors"),
    url(r'^(?P<rhash>[\w-]+)/delete$', delete_exception, name='delete_error'),
    url(r'^(?P<rhash>[\w-]+)$', detail, name='view_error'),
]
