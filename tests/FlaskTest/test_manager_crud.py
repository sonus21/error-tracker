# -*- coding: utf-8 -*-
#
#    Test all end points are working as expected
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#
from .utils import TestCaseMixin


class AppErrorTrackerCrudTest(TestCaseMixin):
    db_prefix = "AppErrorTrackerCrudTest"

    def fire_request(self, db_name):
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
        return error_tracker

    def test_delete(self):
        error_tracker = self.fire_request("test_delete")
        error_tracker.delete_exception(error_tracker.get_exceptions()[0].hash)
        self.assertEqual(len(error_tracker.get_exceptions()), 0)

    def test_get(self):
        error_tracker = self.fire_request("test_get")
        rhash = error_tracker.get_exception(error_tracker.get_exceptions()[0].hash)
        self.assertIsNotNone(rhash)

    def test_create_or_update(self):
        error_tracker = self.fire_request("test_get")
        exception = error_tracker.get_exceptions()[0]
        exception.hash = "test_create_or_update"
        error_tracker.create_or_update_exception(exception.hash, exception.host, exception.path,
                                                 exception.method, exception.request_data,
                                                 exception.exception_name, exception.traceback)
        self.assertIsNotNone(error_tracker.get_exception(exception.hash))
