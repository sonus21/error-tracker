import unittest

from test_basic import StaticTestCase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_error import AppErrorManager


class InitLaterTestCase(StaticTestCase):
    db_prefix = "InitLaterTestCase"

    def _setup(self, db_file):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_file
        db = SQLAlchemy(app)
        error_manager = AppErrorManager()
        error_manager.init_app(app, db)
        db.create_all()
        return app, db, error_manager


if __name__ == '__main__':
    unittest.main()
