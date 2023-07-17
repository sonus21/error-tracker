# -*- coding: utf-8 -*-
#
#    Test custom model features
#
#    :copyright: 2023 Sonu Kumar
#    :license: BSD-3-Clause
#


import unittest
from flask import Flask
from error_tracker import AppErrorTracker
from tests.utils import TestErrorModel
from .test_basic import BasicTest
from tests.utils import ViewPermission


class CustomModelClassTest(BasicTest, unittest.TestCase):
    db_prefix = "CustomModelClassTest"

    def _setup(self, db_name):
        app = Flask(__name__)
        TestErrorModel.delete_all()
        error_tracker = AppErrorTracker(app=app, model=TestErrorModel, view_permission=ViewPermission())
        return app, None, error_tracker


if __name__ == '__main__':
    unittest.main()
