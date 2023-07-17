# -*- coding: utf-8 -*-
#
#    Test manual error tracking is working or not
#
#    :copyright: 2023 Sonu Kumar
#    :license: BSD-3-Clause
#
import unittest

from tests.FlaskTest.utils import TestCaseMixin
from error_tracker import flask_scope


class RecordErrorTest(TestCaseMixin, unittest.TestCase):
    db_prefix = "RecordErrorTest"

    def throw(self):
        password = "qwerty"
        secret = "pass"
        key = "key"
        foo_secret = "THIS IS SECRET"
        test_password_test = "test_password_test"
        TestPassWordTest = "TestPassWordTest"
        TestSecret = "TESTSECRET"
        l = [1, 2, 3, 4]
        t = (1, 2, 3, 4)
        d = {'test': 100, "1": 1000}
        print(password, secret, key, d, foo_secret,
              TestPassWordTest, test_password_test, TestSecret, l, t, d)
        print(d['KeyError'])
        return "KeyError"

    def test_auto_track_exception_decorator(self):
        db_name = "test_tickets_are_raise"
        app, db, error_tracker = self.setUpApp(db_name)

        @error_tracker.auto_track_exception
        def fun(a, b, x="123"):
            print(a, b, x)
            self.throw()

        try:
            fun(1, 2, x="test")
        except Exception as e:
            pass
        self.verify(error_tracker)

    def verify(self, error_tracker, request_date="{}"):
        errors = error_tracker.get_exceptions()
        self.assertEqual(len(errors), 1)
        error = errors[-1]
        self.assertIsNotNone(error.hash)
        self.assertEqual(error.count, 1)
        self.assertEqual(error.method, '')
        self.assertEqual(error.path, "")
        self.assertEqual(error.host, "")
        self.assertEqual(error.request_data, request_date)
        self.assertIsNotNone(error.traceback)
        self.assertIsNotNone(error.created_on)
        self.assertIsNotNone(error.last_seen)

    def test_record(self):
        db_name = "test_tickets_are_raise"
        app, db, error_tracker = self.setUpApp(db_name)
        try:
            self.throw()
        except Exception as e:
            error_tracker.capture_exception()
        self.verify(error_tracker)

    def test_message(self):
        db_name = "test_message"
        app, db, error_tracker = self.setUpApp(db_name)
        try:
            self.throw()
        except Exception as e:
            error_tracker.capture_message("Something went wrong!")
        self.verify(error_tracker, request_date="{'context': {'message': 'Something went wrong!'}}")

    def test_context_manager(self):
        db_name = "context_manager"
        app, db, error_tracker = self.setUpApp(db_name)
        with flask_scope(error_tracker) as scope:
            scope.set_extra("id", 1234)
            self.throw()
        self.verify(error_tracker, request_date="{'context': {'id': 1234}}")

    def test_context_manager_with_initial_context(self):
        db_name = "test_context_manager_with_initial_context"
        app, db, error_tracker = self.setUpApp(db_name)
        with flask_scope(error_tracker, context={"id": 1234}) as scope:
            self.throw()
        self.verify(error_tracker, request_date="{'context': {'id': 1234}}")

    def test_context_manager_exception_not_handled(self):
        db_name = "test_context_manager_exception_not_handled"
        app, db, error_tracker = self.setUpApp(db_name)
        try:
            with flask_scope(error_tracker, handle_exception=False) as scope:
                self.throw()
            self.assertTrue(False)
        except Exception:
            self.verify(error_tracker, request_date="{}")


if __name__ == '__main__':
    unittest.main()
