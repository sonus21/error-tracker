# -*- coding: utf-8 -*-
#
#    Test manual error tracking is working or not
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#
import unittest

from .utils import TestCaseMixin


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

    def verify(self, error_tracker):
        errors = error_tracker.get_exceptions()
        self.assertEqual(len(errors), 1)
        error = errors[-1]
        self.assertIsNotNone(error.hash)
        self.assertEqual(error.count, 1)
        self.assertEqual(error.method, '')
        self.assertEqual(error.path, "")
        self.assertEqual(error.host, "")
        self.assertEqual(error.request_data, "{}")
        self.assertIsNotNone(error.traceback)
        self.assertIsNotNone(error.created_on)
        self.assertIsNotNone(error.last_seen)

    def test_record(self):
        db_name = "test_tickets_are_raise"
        app, db, error_tracker = self.setUpApp(db_name)
        try:
            self.throw()
        except Exception as e:
            error_tracker.record_exception()
        self.verify(error_tracker)


if __name__ == '__main__':
    unittest.main()
