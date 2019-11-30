# -*- coding: utf-8 -*-
#
#    Test custom model features
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#


import unittest

from django.test import LiveServerTestCase

from test_basic import BasicTests
from util import TestBase


class CustomModelClassTest(LiveServerTestCase, TestBase, BasicTests):
    def test_no_exception(self):
        self.no_exception()

    def test_value_error(self):
        from error_tracker import get_exception_model
        model = get_exception_model()
        self.assertEqual("TestErrorModel", model.__name__)
        model.delete_all()

        self.value_error()

    def test_post_method_error(self):
        self.post_method_error()


if __name__ == '__main__':
    unittest.main()
