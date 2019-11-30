# -*- coding: utf-8 -*-
#
#    Test app initialization post constructions
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest

from .test_basic import BasicTest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from error_tracker import AppErrorTracker


class InitLaterTest(BasicTest):
    db_prefix = "InitLaterTest"

    def _setup(self, db_file):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_file
        db = SQLAlchemy(app)
        error_tracker = AppErrorTracker()
        error_tracker.init_app(app, db)
        db.drop_all()
        db.create_all()
        return app, db, error_tracker


if __name__ == '__main__':
    unittest.main()
