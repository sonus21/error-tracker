# -*- coding: utf-8 -*-
#
#    Basic test case test, this tests basic part of application
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#
import unittest

from django.test import LiveServerTestCase
from util import TestBase


class BasicTests(object):
    def no_exception(self):
        result = self.client.get("/")
        self.assertEqual(u'No Exception!', result.content.decode('utf-8'))
        self.assertEqual(self.get_exceptions(), [])

    def value_error(self):
        self.get("/value-error")
        errors = self.get_exceptions()
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertIsNotNone(error.hash)
        self.assertIsNotNone(error.host)
        self.assertIsNotNone(error.path)
        self.assertIsNotNone(error.method)
        self.assertIsNotNone(error.request_data)
        self.assertIsNotNone(error.traceback)
        self.assertIsNotNone(error.count)
        self.assertIsNotNone(error.created_on)
        self.assertIsNotNone(error.last_seen)

        self.assertEqual(error.count, 1)
        self.assertEqual(error.method, 'GET')
        self.assertEqual(error.path, "/value-error")

        self.get('/value-error')
        errors = self.get_exceptions()
        self.assertEqual(len(errors), 1)
        error_new = errors[-1]

        self.assertEqual(error_new.hash, error.hash)
        self.assertEqual(error_new.host, error.host)
        self.assertEqual(error_new.path, error.path)
        self.assertEqual(error_new.method, error.method)
        self.assertEqual(error_new.request_data, error.request_data)
        self.assertEqual(error_new.traceback, error.traceback)
        self.assertNotEqual(error_new.count, error.count)
        self.assertEqual(error_new.created_on, error.created_on)
        self.assertNotEqual(error_new.last_seen, error.last_seen)
        self.assertEqual(error_new.count, 2)

        self.get('/value-error')
        errors = self.get_exceptions()
        self.assertEqual(len(errors), 1)
        error_new = errors[-1]
        self.assertEqual(error_new.count, 3)

    def post_method_error(self):
        self.post('/post-view')
        errors = self.get_exceptions()
        self.assertEqual(len(errors), 1)
        error = errors[-1]
        self.assertIsNotNone(error.hash)
        self.assertIsNotNone(error.host)
        self.assertIsNotNone(error.path)
        self.assertIsNotNone(error.method)
        self.assertIsNotNone(error.request_data)
        self.assertIsNotNone(error.traceback)
        self.assertIsNotNone(error.count)
        self.assertIsNotNone(error.created_on)
        self.assertIsNotNone(error.last_seen)
        self.assertEqual(error.count, 1)
        self.assertEqual(error.method, 'POST')
        self.assertEqual(error.path, "/post-view")


class BasicTestCase(LiveServerTestCase, TestBase, BasicTests):

    def test_no_exception(self):
        self.no_exception()

    def test_value_error(self):
        self.value_error()

    def test_post_method_error(self):
        self.post_method_error()


if __name__ == '__main__':
    unittest.main()
