# -*- coding: utf-8 -*-
#
#    Test utils
#
#    :copyright: 2023 Sonu Kumar
#    :license: BSD-3-Clause
#

from error_tracker.django import get_exception_model
from error_tracker.django.middleware import notifier


class TestBase(object):

    def get_exceptions(self):
        model = get_exception_model()
        return list(model.get_exceptions_per_page().items)

    def create_or_update_exception(self, rhash, host, path, method, request_data, exception_name, traceback):
        model = get_exception_model()
        return model.create_or_update_entity(rhash, host, path, method, request_data, exception_name, traceback)

    def get_notifications(self):
        return notifier.get_notifications()

    def clear_notifications(self):
        return notifier.clear()

    def get(self, path, **kwargs):
        try:
            return self.client.get(path, **kwargs)
        except Exception as e:
            print(e)
            return None

    def post(self, path, **kwargs):
        try:
            return self.client.post(path, **kwargs)
        except Exception as e:
            print(e)
            return None
