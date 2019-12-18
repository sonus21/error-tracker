# -*- coding: utf-8 -*-
#
#    Test Django Rest framework related changes
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest

from django.test import LiveServerTestCase
from util import TestBase


class BasicTestCase(LiveServerTestCase, TestBase):

    def test_no_exception(self):
        result = self.client.get("/users/")
        self.assertEqual(u'[]', result.content.decode('utf-8'))
        self.assertEqual(self.get_exceptions(), [])

    def test_create_user(self):
        from_data = {'username': 'admin', 'email': 'example@example.com'}
        self.post("/users/", data=from_data)
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
        form = eval(error.request_data)['form']
        self.assertEqual(from_data, form)


if __name__ == '__main__':
    unittest.main()
