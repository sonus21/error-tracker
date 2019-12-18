# -*- coding: utf-8 -*-
#
#    Test view permission feature
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#


import unittest

from flask import Flask

from error_tracker import AppErrorTracker
from tests.utils import TestErrorModel
from .utils import BaseTestMixin


class View401Test(BaseTestMixin):
    db_prefix = "View401"

    def _setup(self, db_name):
        app = Flask(__name__)
        TestErrorModel.delete_all()
        error_tracker = AppErrorTracker(app=app, model=TestErrorModel)
        return app, None, error_tracker

    def verify(self, db_name, url):
        app, db, _ = self.setUpApp(db_name)
        with app.test_client() as c:
            response = c.get(url, follow_redirects=True)
            self.assertEquals(response.status_code, 401)

    def test_list_view(self):
        self.verify("test_list_view", '/dev/error')

    def test_detail_view(self):
        self.verify("test_detail_view", '/dev/error/xyz')

    def test_delete_view(self):
        self.verify("test_delete_view", '/dev/error/delete/xyz')


if __name__ == '__main__':
    unittest.main()
