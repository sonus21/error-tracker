# -*- coding: utf-8 -*-
#
#    Basic test case test, this tests basic part of application
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#
import unittest

from django.test import LiveServerTestCase
from util import TestBase
from error_tracker import track_exception, capture_exception, capture_message, configure_scope


class RecordErrorTest(LiveServerTestCase, TestBase):
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

    def verify(self, data="{}"):
        errors = self.get_exceptions()
        self.assertEqual(len(errors), 1)
        error = errors[-1]
        self.assertIsNotNone(error.hash)
        self.assertEqual(error.count, 1)
        self.assertEqual(error.method, '')
        self.assertEqual(error.path, "")
        self.assertEqual(error.host, "")
        self.assertEqual(error.request_data, data)
        self.assertIsNotNone(error.traceback)
        self.assertIsNotNone(error.created_on)
        self.assertIsNotNone(error.last_seen)

    def test_decorator_recording(self):
        @track_exception
        def fun(a, b, x=123):
            print(a, b, x)
            self.throw()

        try:
            fun(1, 2, x=456)
        except Exception:
            pass
        self.verify()

    def test_record(self):
        try:
            self.throw()
        except Exception as e:
            capture_exception(None, e)
        self.verify()

    def test_message(self):
        try:
            self.throw()
        except Exception:
            capture_message("Something went wrong.")
        self.verify(data="{'context': {'message': 'Something went wrong.'}}")

    def test_additional_context(self):
        with configure_scope() as f:
            f.set_extra("id", 1234)
            self.throw()
        self.verify(data="{'context': {'id': 1234}}")

    def test_context_manager_exception_not_handled(self):
        try:
            with configure_scope(handle_exception=False) as f:
                f.set_extra("id", 1234)
                self.throw()
            self.assertTrue(False)
        except Exception:
            self.verify(data="{'context': {'id': 1234}}")
            pass

    def test_context_manager_with_initial_context(self):
        try:
            with configure_scope(context={"id": 1234}) as f:
                self.throw()
            self.assertTrue(False)
        except Exception:
            self.verify(data="{'context': {'id': 1234}}")


if __name__ == '__main__':
    unittest.main()
