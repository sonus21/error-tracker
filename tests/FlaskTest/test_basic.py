# -*- coding: utf-8 -*-
#
#    Basic test case test, this tests basic part of application
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#
import unittest
from .utils import TestCaseMixin


class BasicTest(TestCaseMixin):
    db_prefix = "BasicTest"

    def test_no_exception(self):
        db_file = "test_no_exception"
        app, db, error_tracker = self.setUpApp(db_file)
        with app.test_client() as c:
            result = c.get('/')
            self.assertEqual(u'No Exception!', result.data.decode('utf-8'))
            self.assertEqual(error_tracker.get_exceptions(), [])

    def test_value_error(self):
        db_name = "test_value_error"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            result = c.get('/value-error')
            self.assertEqual(u'500', result.data.decode('utf-8'))
            errors = error_tracker.get_exceptions()
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

            c.get('/value-error')
            errors = error_tracker.get_exceptions()
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

            c.post('/value-error')
            errors = error_tracker.get_exceptions()
            self.assertEqual(len(errors), 1)
            error_new = errors[-1]
            self.assertEqual(error_new.count, 3)

    def test_post_method_error(self):
        db_name = "post_method_error"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            c.post('/post-view')
            errors = error_tracker.get_exceptions()
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


if __name__ == '__main__':
    unittest.main()
